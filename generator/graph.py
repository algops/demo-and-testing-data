"""Phase 1: relationship graph generation."""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .catalogues import DOMAIN_AGENTS, DOMAIN_INTEGRATIONS, TYPE_REFRAME, _load_domain_spec, get_kb_doc_specs
from .semantic.edge_values import materialize_edge_values
from .semantic.example_pools import build_instance
from .semantic.org_names import (
    ORG_EMPLOYEE_ATTRS,
    ORG_KPI_ATTRS,
    ORG_PERSON_ATTRS,
    ORG_TEAM_ATTRS,
    ORG_TEAM_NAMES,
    generate_employee_attrs,
    generate_org_kpi_values,
    generate_person_attrs,
    generate_team_attrs,
)
from .attribute_types import ValueScalar
from .util import (
    DOMAINS,
    NOW,
    ORG_ID,
    SHARED,
    load_yaml_simple,
    make_id,
    parse_range,
    slugify,
    ROOT,
)

ORG_TYPES = {
    "organization": {"label": "Organizace", "count": 1},
    "person": {"label": "Osoba", "count": 220},
    "employee": {"label": "Zaměstnanec", "count": 200},
    "department": {"label": "Oddělení", "count": 10},
    "team": {"label": "Tým", "count": 12},
    "system": {"label": "Systém", "count": 12},
    "vendor": {"label": "Dodavatel", "count": 5},
}

SYSTEM_NAMES = [
    "GitLab",
    "Confluence",
    "Slack",
    "Datadog",
    "PagerDuty",
    "iManage",
    "SharePoint",
    "SAP SuccessFactors",
    "Recruitee",
    "Pohoda",
    "Sphera",
    "EPO",
]

VENDOR_NAMES = [
    ("kovar-partners", "Kovář & Partners advokátní kancelář s.r.o."),
    ("financni-centrum", "Finanční Centrum s.r.o."),
    ("deloitte-cz", "Deloitte CZ"),
    ("benefity-as", "Benefity a.s."),
    ("sodexo", "Sodexo CZ"),
]

DEPT_NAMES = [
    "Engineering",
    "Product",
    "Operations",
    "Risk & Compliance",
    "Finance",
    "People",
    "ESG",
    "Sales",
    "G&A",
    "Legal",
]


@dataclass
class GraphState:
    relationships: list[dict[str, Any]] = field(default_factory=list)
    object_type_ids: dict[str, str] = field(default_factory=dict)
    datapoint_ids: dict[str, str] = field(default_factory=dict)
    object_ids: dict[str, str] = field(default_factory=dict)
    objects_by_type: dict[str, list[str]] = field(default_factory=dict)
    integration_ids: dict[str, str] = field(default_factory=dict)
    agent_ids: dict[str, str] = field(default_factory=dict)
    value_ids: list[str] = field(default_factory=list)
    kb_folder_ids: dict[str, str] = field(default_factory=dict)
    kb_doc_ids: dict[str, str] = field(default_factory=dict)
    kb_doc_meta: dict[str, dict[str, Any]] = field(default_factory=dict)
    object_names: dict[str, str] = field(default_factory=dict)
    object_attr_values: dict[str, dict[str, ValueScalar]] = field(default_factory=dict)
    value_payloads: dict[str, ValueScalar] = field(default_factory=dict)
    value_meta: dict[str, dict[str, str]] = field(default_factory=dict)
    rng: random.Random = field(default_factory=lambda: random.Random(42))

    def add_rel(
        self,
        origin_type: str,
        origin_id: str,
        dest_type: str,
        dest_id: str,
        kind: str,
        meta: dict | None = None,
    ) -> None:
        edge = {
            "origin_type": origin_type,
            "origin_id": origin_id,
            "destination_type": dest_type,
            "destination_id": dest_id,
            "relationship_kind": kind,
        }
        if meta:
            edge["metadata"] = meta
        self.relationships.append(edge)


def _type_key(domain: str, type_name: str) -> str:
    return f"{domain}:{slugify(type_name)}"


def _object_seed(domain: str, type_name: str, index: int) -> str:
    return f"org:anchor:{domain}:{slugify(type_name)}:{index:04d}"


def _shared_seed(entity: str, slug: str) -> str:
    return f"org:anchor:shared:{entity}:{slug}"


def load_blueprint(domain: str) -> dict[str, Any]:
    return load_yaml_simple(ROOT / "blueprints" / "domains" / f"{domain}.yaml")


def _ensure_datapoints(
    state: GraphState,
    type_key: str,
    domain: str,
    type_slug: str,
    attrs: list[str],
) -> None:
    ot_id = state.object_type_ids.get(type_key)
    if not ot_id:
        ot_id = make_id(f"object-type:{domain}:{type_slug}")
        state.object_type_ids[type_key] = ot_id
    for attr in attrs:
        dp_key = f"{type_key}:{attr}"
        if dp_key in state.datapoint_ids:
            continue
        dp_id = make_id(f"datapoint:{domain}:{type_slug}:{attr}")
        state.datapoint_ids[dp_key] = dp_id
        state.add_rel("object-type", ot_id, "datapoint", dp_id, "defines_schema")


def _emit_object_values(
    state: GraphState,
    oid: str,
    type_key: str,
    attr_values: dict[str, ValueScalar],
    seed_prefix: str,
) -> None:
    for attr, payload in attr_values.items():
        dp_key = f"{type_key}:{attr}"
        dp_id = state.datapoint_ids.get(dp_key)
        if not dp_id:
            continue
        val_id = make_id(f"value:{seed_prefix}:{attr}")
        state.value_ids.append(val_id)
        state.value_payloads[val_id] = payload
        state.value_meta[val_id] = {"object_id": oid, "datapoint_id": dp_id}
        state.add_rel("object", oid, "value", val_id, "has_value")
        state.add_rel("datapoint", dp_id, "value", val_id, "value_of")


def _add_domain_edge(
    state: GraphState,
    origin_oid: str,
    dest_oid: str,
    rel_spec: dict[str, Any],
    domain: str,
    edge_index: int,
    extra_meta: dict[str, Any] | None = None,
) -> None:
    meta: dict[str, Any] = {"domain_edge": rel_spec["type"], "domain_id": domain}
    if extra_meta:
        meta.update(extra_meta)
    edge_values = materialize_edge_values(state, origin_oid, rel_spec, domain, edge_index)
    meta["edge_values"] = edge_values
    state.add_rel("object", origin_oid, "object", dest_oid, "related_to", meta)


def emit_org_layer(state: GraphState) -> None:
    org_oid = make_id(_shared_seed("organization", "meridian-pay"))
    state.object_ids["shared:organization:meridian-pay"] = org_oid
    state.objects_by_type.setdefault("shared:organization", []).append(org_oid)

    ot_org = make_id("object-type:shared:organization")
    state.object_type_ids["shared:organization"] = ot_org
    state.add_rel("object-type", ot_org, "object", org_oid, "has_instance")
    state.add_rel("object", org_oid, "object-type", ot_org, "instance_of")

    for slug, label in [
        ("organization", "Organizace"),
        ("person", "Osoba"),
        ("employee", "Zaměstnanec"),
        ("department", "Oddělení"),
        ("team", "Tým"),
        ("system", "Systém"),
        ("vendor", "Dodavatel"),
    ]:
        ot = make_id(f"object-type:shared:{slug}")
        state.object_type_ids[f"shared:{slug}"] = ot

    _ensure_datapoints(state, "shared:person", SHARED, "person", ORG_PERSON_ATTRS)
    _ensure_datapoints(state, "shared:employee", SHARED, "employee", ORG_EMPLOYEE_ATTRS)
    _ensure_datapoints(state, "shared:team", SHARED, "team", ORG_TEAM_ATTRS)
    _ensure_datapoints(state, "shared:organization", SHARED, "organization", ORG_KPI_ATTRS)

    state.object_names["shared:organization:meridian-pay"] = "Meridian Pay a.s."
    kpi_values = generate_org_kpi_values(state.rng)
    state.object_attr_values["shared:organization:meridian-pay"] = kpi_values
    _emit_object_values(
        state,
        org_oid,
        "shared:organization",
        kpi_values,
        _shared_seed("organization", "meridian-pay"),
    )

    person_attrs_by_key: dict[str, dict[str, str]] = {}
    for i in range(ORG_TYPES["person"]["count"]):
        slug = f"person-{i + 1:04d}"
        oid = make_id(_shared_seed("person", slug))
        key = f"shared:person:{slug}"
        state.object_ids[key] = oid
        state.objects_by_type.setdefault("shared:person", []).append(oid)
        ot = state.object_type_ids["shared:person"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")
        attrs = generate_person_attrs(i, state.rng)
        person_attrs_by_key[key] = attrs
        display = f"{attrs['first_name']} {attrs['last_name']}"
        state.object_names[key] = display
        state.object_attr_values[key] = attrs
        _emit_object_values(state, oid, "shared:person", attrs, _shared_seed("person", slug))

    for i in range(ORG_TYPES["employee"]["count"]):
        slug = f"employee-{i + 1:04d}"
        oid = make_id(_shared_seed("employee", slug))
        key = f"shared:employee:{slug}"
        state.object_ids[key] = oid
        state.objects_by_type.setdefault("shared:employee", []).append(oid)
        ot = state.object_type_ids["shared:employee"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")
        person_key = f"shared:person:person-{min(i + 1, ORG_TYPES['person']['count']):04d}"
        person_attrs = person_attrs_by_key.get(
            person_key, generate_person_attrs(i, state.rng)
        )
        attrs = generate_employee_attrs(i, person_attrs, state.rng)
        display = f"{person_attrs['first_name']} {person_attrs['last_name']}"
        state.object_names[key] = display
        state.object_attr_values[key] = attrs
        _emit_object_values(state, oid, "shared:employee", attrs, _shared_seed("employee", slug))
        if state.objects_by_type.get("shared:person"):
            pid = state.object_ids.get(person_key) or state.rng.choice(
                state.objects_by_type["shared:person"]
            )
            state.add_rel("object", oid, "object", pid, "related_to", {"bridge": "employee_person"})

    for i, name in enumerate(DEPT_NAMES):
        slug = slugify(name)
        oid = make_id(_shared_seed("department", slug))
        key = f"shared:department:{slug}"
        state.object_ids[key] = oid
        state.object_names[key] = name
        state.objects_by_type.setdefault("shared:department", []).append(oid)
        ot = state.object_type_ids["shared:department"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")
        state.add_rel("object", org_oid, "object", oid, "related_to", {"bridge": "org_department"})

    for i in range(ORG_TYPES["team"]["count"]):
        team_name = ORG_TEAM_NAMES[i % len(ORG_TEAM_NAMES)]
        slug = slugify(team_name)
        oid = make_id(_shared_seed("team", slug))
        key = f"shared:team:{slug}"
        state.object_ids[key] = oid
        state.objects_by_type.setdefault("shared:team", []).append(oid)
        ot = state.object_type_ids["shared:team"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")
        attrs = generate_team_attrs(team_name, i, state.rng)
        state.object_names[key] = team_name
        state.object_attr_values[key] = attrs
        _emit_object_values(state, oid, "shared:team", attrs, _shared_seed("team", slug))

    for i, sys_name in enumerate(SYSTEM_NAMES):
        slug = slugify(sys_name)
        oid = make_id(_shared_seed("system", slug))
        key = f"shared:system:{slug}"
        state.object_ids[key] = oid
        state.object_names[key] = sys_name
        state.objects_by_type.setdefault("shared:system", []).append(oid)
        ot = state.object_type_ids["shared:system"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")

    for slug, name in VENDOR_NAMES:
        oid = make_id(_shared_seed("vendor", slug))
        key = f"shared:vendor:{slug}"
        state.object_ids[key] = oid
        state.object_names[key] = name
        state.objects_by_type.setdefault("shared:vendor", []).append(oid)
        ot = state.object_type_ids["shared:vendor"]
        state.add_rel("object-type", ot, "object", oid, "has_instance")
        state.add_rel("object", oid, "object-type", ot, "instance_of")


def emit_domain(state: GraphState, domain: str) -> None:
    types, rels = _load_domain_spec(domain)
    blueprint = load_blueprint(domain)
    counts: dict[str, str | int] = blueprint.get("object_counts", {})

    for et in types:
        tname = et["type"]
        tslug = slugify(tname)
        tk = _type_key(domain, tname)
        ot_id = make_id(f"object-type:{domain}:{tslug}")
        state.object_type_ids[tk] = ot_id

        for attr in et.get("attributes", []):
            dp_key = f"{tk}:{attr}"
            dp_id = make_id(f"datapoint:{domain}:{tslug}:{attr}")
            state.datapoint_ids[dp_key] = dp_id
            state.add_rel("object-type", ot_id, "datapoint", dp_id, "defines_schema")

        count = parse_range(counts.get(tslug, counts.get(tname, 5)))
        if tslug not in counts and slugify(tname) not in counts:
            count = min(count, 8)
        state.objects_by_type.setdefault(tk, [])
        examples = et.get("examples", [])
        attributes = et.get("attributes", [])
        pool_size = len(examples) if examples else 1
        for i in range(count):
            seed = _object_seed(domain, tname, i)
            oid = make_id(seed)
            okey = f"{domain}:{tslug}:{i:04d}"
            state.object_ids[okey] = oid
            state.objects_by_type[tk].append(oid)
            state.add_rel("object-type", ot_id, "object", oid, "has_instance")
            state.add_rel("object", oid, "object-type", ot_id, "instance_of")

            example = examples[i % pool_size] if examples else f"{tname} {i + 1}"
            display, attr_values = build_instance(
                example, attributes, tslug, domain, i, pool_size, state.rng
            )
            state.object_names[okey] = display
            state.object_attr_values[okey] = attr_values
            _emit_object_values(state, oid, tk, attr_values, seed)

    edge_counter = 0
    for r in rels:
        from_types = r["from"] if isinstance(r["from"], list) else [r["from"]]
        to_type = r["to"]
        from_tk = _type_key(domain, from_types[0])
        to_tk = _type_key(domain, to_type)
        from_list = state.objects_by_type.get(from_tk, [])
        to_list = state.objects_by_type.get(to_tk, [])
        if not from_list or not to_list:
            continue
        n = min(len(from_list), max(4, len(from_list) // 5))
        for _ in range(n):
            fo = state.rng.choice(from_list)
            to = state.rng.choice(to_list)
            if fo == to:
                continue
            _add_domain_edge(state, fo, to, r, domain, edge_counter)
            edge_counter += 1

    for spec in DOMAIN_INTEGRATIONS[domain]:
        slug = slugify(spec["name"])
        iid = make_id(f"integration:{domain}:{slug}")
        state.integration_ids[f"{domain}:{slug}"] = iid
        ot_int = make_id(f"object-type:integration:{domain}")
        if f"meta:integration:{domain}" not in state.object_type_ids:
            state.object_type_ids[f"meta:integration:{domain}"] = ot_int


def emit_org_bridges(state: GraphState) -> None:
    org_oid = state.objects_by_type["shared:organization"][0]
    employees = state.objects_by_type.get("shared:employee", [])
    vendors = state.objects_by_type.get("shared:vendor", [])
    systems = state.objects_by_type.get("shared:system", [])

    bridge_targets = {
        "it": ["it:service", "it:incident"],
        "legal": ["legal:matter", "legal:contract"],
        "tax": ["tax:engagement", "tax:legal_entity"],
        "hr": ["hr:policy", "hr:process"],
        "esg": ["esg:report", "esg:metric"],
    }

    for domain, type_keys in bridge_targets.items():
        for tk in type_keys:
            objs = state.objects_by_type.get(tk, [])
            if not objs:
                continue
            for _ in range(min(5, len(objs))):
                emp = state.rng.choice(employees) if employees else None
                obj = state.rng.choice(objs)
                if emp:
                    state.add_rel("object", emp, "object", obj, "related_to", {"bridge": "employee_domain"})
                state.add_rel("object", org_oid, "object", obj, "related_to", {"bridge": "org_scope"})

    kovar = state.object_ids.get("shared:vendor:kovar_partners") or state.object_ids.get(
        "shared:vendor:kovar-partners"
    )
    if not kovar:
        for k, v in state.object_ids.items():
            if "kovar" in k:
                kovar = v
                break
    matters = state.objects_by_type.get("legal:matter", [])
    if kovar and matters:
        for m in matters[:8]:
            state.add_rel("object", m, "object", kovar, "related_to", {"bridge": "external_counsel"})

    fin = None
    for k, v in state.object_ids.items():
        if "financni" in k:
            fin = v
            break
    engagements = state.objects_by_type.get("tax:engagement", [])
    if fin and engagements:
        for e in engagements[:5]:
            state.add_rel("object", e, "object", fin, "related_to", {"bridge": "tax_advisor"})

    for domain in DOMAINS:
        int_key = f"{domain}:{slugify(DOMAIN_INTEGRATIONS[domain][0]['name'])}"
        iid = state.integration_ids.get(int_key)
        if iid and systems:
            sys_oid = state.rng.choice(systems)
            state.add_rel("integration", iid, "object", sys_oid, "related_to", {"bridge": "implements"})


def emit_kb_structure(state: GraphState, min_docs: dict[str, int]) -> None:
    root_id = make_id("knowledge-folder:knowledgebase")
    state.kb_folder_ids["knowledgebase"] = root_id
    org_ot = state.object_type_ids["shared:organization"]
    state.add_rel("object-type", org_ot, "knowledge-folder", root_id, "root_folder")

    for domain in DOMAINS:
        dom_folder = make_id(f"knowledge-folder:knowledgebase/{domain}")
        state.kb_folder_ids[f"knowledgebase/{domain}"] = dom_folder
        state.add_rel("knowledge-folder", root_id, "knowledge-folder", dom_folder, "contains_folder")

        doc_specs = get_kb_doc_specs(domain, min_docs.get(domain, 10))
        folder_cache: dict[str, str] = {}

        def ensure_folder(folder_path: str) -> str:
            if folder_path in state.kb_folder_ids:
                return state.kb_folder_ids[folder_path]
            parts = folder_path.split("/")
            parent_path = "/".join(parts[:-1])
            parent_id = ensure_folder(parent_path) if parent_path else root_id
            fid = make_id(f"knowledge-folder:{folder_path}")
            state.kb_folder_ids[folder_path] = fid
            state.add_rel("knowledge-folder", parent_id, "knowledge-folder", fid, "contains_folder")
            folder_cache[folder_path] = fid
            return fid

        for i, spec in enumerate(doc_specs):
            section = spec["section"]
            sub = spec["sub"]
            kind = spec["kind"]
            rel_path = f"{section}/{sub}/{kind}-{i + 1:03d}.md"
            folder_path = f"knowledgebase/{domain}/{section}/{sub}"
            sub_id = ensure_folder(folder_path)
            doc_slug = rel_path.replace(".md", "").replace("/", "-")
            doc_id = make_id(f"knowledge-doc:{domain}:{doc_slug}")
            key = f"{domain}:{doc_slug}"
            state.kb_doc_ids[key] = doc_id
            state.kb_doc_meta[key] = {
                "title": spec["title"],
                "doc_kind": kind,
                "rel_path": rel_path,
                "section": section,
                "sub": sub,
            }
            state.add_rel("knowledge-folder", sub_id, "knowledge-doc", doc_id, "contains_doc")

            int_slug = slugify(DOMAIN_INTEGRATIONS[domain][0]["name"])
            iid = state.integration_ids.get(f"{domain}:{int_slug}")
            if iid:
                state.add_rel("integration", iid, "knowledge-doc", doc_id, "syncs")


def build_relationship_graph(min_docs: dict[str, int]) -> GraphState:
    state = GraphState()
    emit_org_layer(state)
    for domain in DOMAINS:
        emit_domain(state, domain)
    emit_org_bridges(state)
    emit_kb_structure(state, min_docs)

    for domain in DOMAINS:
        dom_folder = state.kb_folder_ids.get(f"knowledgebase/{domain}")
        domain_docs = [k for k in state.kb_doc_ids if k.startswith(f"{domain}:")]
        tools = [
            s for s in DOMAIN_INTEGRATIONS[domain] if s["role"] == "tool"
        ]
        for spec in DOMAIN_AGENTS[domain]:
            agent_slug = slugify(spec["name"])
            aid = make_id(f"agent:{domain}:{agent_slug}")
            state.agent_ids[f"{domain}:{agent_slug}"] = aid
            if dom_folder:
                state.add_rel("agent", aid, "knowledge-folder", dom_folder, "scoped_to")
            for dk in domain_docs[:4]:
                state.add_rel("agent", aid, "knowledge-doc", state.kb_doc_ids[dk], "reads")
            if tools:
                tool_slug = slugify(tools[0]["name"])
                tid = state.integration_ids.get(f"{domain}:{tool_slug}")
                if tid:
                    state.add_rel("agent", aid, "integration", tid, "uses_tool")

    padding_start = len(state.relationships)
    pad_edge_counter = 100_000
    if len(state.relationships) < 2500:
        attempts = 0
        while len(state.relationships) < 2500 and attempts < 5000:
            attempts += 1
            domain = state.rng.choice(list(DOMAINS))
            _, rels = _load_domain_spec(domain)
            if not rels:
                break
            r = state.rng.choice(rels)
            from_types = r["from"] if isinstance(r["from"], list) else [r["from"]]
            from_tk = _type_key(domain, from_types[0])
            to_tk = _type_key(domain, r["to"])
            from_list = state.objects_by_type.get(from_tk, [])
            to_list = state.objects_by_type.get(to_tk, [])
            if from_list and to_list:
                fo = state.rng.choice(from_list)
                to = state.rng.choice(to_list)
                if fo != to:
                    _add_domain_edge(
                        state,
                        fo,
                        to,
                        r,
                        domain,
                        pad_edge_counter,
                        {"padding": True},
                    )
                    pad_edge_counter += 1

    state.relationships = _truncate_relationships(state.relationships, padding_start)
    state.relationships = _reorder_relationships(state.relationships)
    return state


SEMANTIC_KINDS = {
    "contains_folder",
    "contains_doc",
    "root_folder",
    "scoped_to",
    "reads",
    "syncs",
    "uses_tool",
}

STRUCTURAL_KINDS = {"has_instance", "instance_of", "defines_schema"}
VALUE_KINDS = {"has_value", "value_of"}
VALUE_EDGE_BUDGET = 1000
MAX_VALUES_PER_OBJECT = 3


def _is_must_keep_edge(rel: dict[str, Any]) -> bool:
    kind = rel.get("relationship_kind")
    meta = rel.get("metadata") or {}
    if kind == "related_to" and (meta.get("domain_edge") or meta.get("bridge")):
        return True
    if kind in SEMANTIC_KINDS:
        return True
    if kind in STRUCTURAL_KINDS:
        return True
    if rel.get("origin_type") in ("agent", "integration", "knowledge-folder", "knowledge-doc"):
        return True
    if rel.get("destination_type") in ("agent", "integration", "knowledge-folder", "knowledge-doc"):
        return True
    return False


def _sample_value_edges(value_rels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    has_value_by_object: dict[str, list[dict[str, Any]]] = defaultdict(list)
    value_of_by_value: dict[str, dict[str, Any]] = {}
    for rel in value_rels:
        kind = rel.get("relationship_kind")
        if kind == "has_value":
            has_value_by_object[rel["origin_id"]].append(rel)
        elif kind == "value_of":
            value_of_by_value[rel["destination_id"]] = rel

    kept_has_value: list[dict[str, Any]] = []
    for edges in has_value_by_object.values():
        for rel in edges[:MAX_VALUES_PER_OBJECT]:
            kept_has_value.append(rel)
            if len(kept_has_value) >= VALUE_EDGE_BUDGET:
                break
        if len(kept_has_value) >= VALUE_EDGE_BUDGET:
            break

    kept: list[dict[str, Any]] = []
    for rel in kept_has_value:
        kept.append(rel)
        value_of = value_of_by_value.get(rel["destination_id"])
        if value_of:
            kept.append(value_of)
    return kept


def _truncate_relationships(rels: list[dict[str, Any]], padding_start: int) -> list[dict[str, Any]]:
    anchor = load_yaml_simple(ROOT / "blueprints" / "anchor.yaml")
    max_edges = int(anchor.get("generation", {}).get("max_edges", 10000))

    must_keep: list[dict[str, Any]] = []
    value_rels: list[dict[str, Any]] = []
    optional: list[dict[str, Any]] = []

    for idx, rel in enumerate(rels):
        meta = rel.get("metadata") or {}
        if idx >= padding_start and meta.get("padding"):
            continue
        if _is_must_keep_edge(rel):
            must_keep.append(rel)
        elif rel.get("relationship_kind") in VALUE_KINDS:
            value_rels.append(rel)
        else:
            optional.append(rel)

    result = list(must_keep)
    result.extend(_sample_value_edges(value_rels))

    for rel in optional:
        if len(result) >= max_edges:
            break
        result.append(rel)

    if len(result) > max_edges:
        result = result[:max_edges]

    return result


def _edge_priority(rel: dict[str, Any]) -> int:
    meta = rel.get("metadata") or {}
    kind = rel.get("relationship_kind")
    if kind == "related_to" and meta.get("domain_edge"):
        return 0
    if kind == "related_to" and meta.get("bridge"):
        return 1
    if kind in SEMANTIC_KINDS:
        return 2
    if kind in STRUCTURAL_KINDS:
        return 3
    if kind in VALUE_KINDS:
        return 4
    return 5


def _reorder_relationships(rels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for rel in rels:
        buckets[_edge_priority(rel)].append(rel)
    ordered: list[dict[str, Any]] = []
    for priority in sorted(buckets):
        ordered.extend(buckets[priority])
    return ordered
