# Product AI flow

## **Specs for AI guidelines**

**→ machines first, humans second**.


**Goals:**

* Specs are unambiguous
* AI tools (e.g., Claude Code) can generate correct implementation
* Devs don't need to interpret intent
* QA knows exactly what to test


**Rules:**


1. Follow the regular template of the epic / issue that we have defined.
2. Be deterministic - no room for interpretation left.
3. Do NOT Use Technical Field Names in the specs. AI should follow the development rules and patterns of already existing terms. If we give them incorrect patterns or names those would be unnecessarily blindly followed.
4. Designs / prototypes:

   
   1. If you have figma designs - those can be linked, devs would access them through MCP.
   2. **\[FURTHER EXPERIMENTING AND SOLUTION NEEDED\]** If you have figma make prototype - exporting to figma wouldn't work well for AI as components would be bad. In such case it's better to use flat printscreens within the specs.

      **// experiment1 idea: try reusing prompts from figma make within claude?**

      **// experiment2 idea: use figma make from the claude copilot**
   3. Ensure the specs text is matching 1:1 the desgins/prototype.
5. Acceptance criteria for 
6. Keep post-MVP future scope and vision references clearly separated in the dedicated Post-MVP section. Avoid any sort of Post-MVP references in the scope description as it may be very misleading for the AI.
7. When you consider your specs are 'ready' always double check with your AI agent for any gaps or ambiguities. Correct if needed!


**More rules and flow ideas / points to discuss:**

* …
* …
* …


## Next steps

**OBSOLETE - To add to dev flow part:**

- [ ] QA guidelines and acceptance criteria for each issue → prepared in the ''Plan'' mode for each issue (when those are being created) NOT after the code is done and CRed;

  \

**TODO - To resolve conflicts between ongoing MD initiatives vs Dev AI flow:**

- [ ] Splitting issues into FE and BE : increased control, but idea conflicting with AI flow
- [ ] Splitting epics into the issues : according to the AI Flow process still developers should be doing that (with support of the AI agent shall be doing that

* QA - break the epics into 'testable' chunks **→ move directly from CR to deployment for non-testable issues?**


**TODOS AFTER PRODUCT MEETING 19/02:**

- [ ] Setup Claude app @[Agnieszka Kołakowska](mention://7f4f58d8-5524-4166-b549-8858d2eb1f64/user/4cb17242-f02a-4cd4-8ae9-de12013bcd14) @[Katarzyna Raczkowska](mention://62ff4115-6580-4c25-a707-81382ecbabe4/user/6bdbcc6b-6a72-4ec2-9137-3f91ce93f45a) 
- [x] Test / Set up shared folders which would be feeding the AI → Google Drive? @[Štěpán Unar](mention://9144637b-f207-4ddf-ba46-17a331cba064/user/b0ae7bcb-a42f-4d98-8b2d-2d172d359319) 
- [x] Guidelines for writing specs for AI  @[Agnieszka Kołakowska](mention://f94c09a4-79a1-41e6-872d-92276c319b6f/user/4cb17242-f02a-4cd4-8ae9-de12013bcd14) 
- [ ] Explore further the Claude prototyping → passing in this form to devs @[Agnieszka Kołakowska](mention://8bf26356-f01e-4827-895f-b99319bade4b/user/4cb17242-f02a-4cd4-8ae9-de12013bcd14) @[Štěpán Unar](mention://70380b96-ace1-4580-b35b-9ffe7e2263c4/user/b0ae7bcb-a42f-4d98-8b2d-2d172d359319) 


\