# Estimations - how to

## New project

### When client does not pay for the discovery package (example: EDRI)

* Discovery roughly what the project is about - ask a lot! figure out which things could make it much more complex than you may thing. Examples: locales, CMSs, integrations with other systems, currencies & time zones, in how many regions it operates?, who's going to be responsible for translations and content, file uploads, AI integrations, just desktop or mobile, if mobile native or responsive web app? etc.
* Do the discovery with Tony.  
* Remember to make budget for the following

  
   1. Project setup (DevOps): decision on infra, setting up infra, pipelines, etc. —> Responsible person: Honza/Milutin
   2. Project setup (devs): decision on tech stack, UI libraries, setting up repo, project , etc. —> Responsible person: Honza + Lukas
   3. Architecture setup: drawing db structure, deciding architecture stuff —> Responsible person: Tony
   4. Design setup: Gathering brand materials, adding it to Figma, creating components, setting up Figma from scratch for certain project —> Responsible person: Design Lead
   5. Product setup (2MDs): establish communication channels & onboarding clients on it, setup gitlab, create documentation, establish next steps, recurring meeitngs (regular client syncs, internal standups, sprints, etc.)
   6. ==Whole team standups? where will this time go?? Devs, QA, PM.==
   7. Product discovery: try to map out the amount of epics / features (in case of web apps) and for each feature count approx 0.5-1MD for discovering it, 1MD for brainstorming it + feedbacking design + validating with client, 0.5-1MD for specifying it, 0.5MD for coordinating all the work around it in dev, 0.5MD for testing/handover to client.  The amounts are arbitrary, and depending on the complexity you should always adjust them. 3-3.5MD per epic should be the average, it includes all the project management and handovers. Responsible person —> POs
   8. Product discovery (in case of landing pages). If there are no features involved, but it's "just a landing page" let designers and developers scope their work, and add \~10-20% (depending on how difficult is the client) for managing the project. If the client is responsive and cooperative, 10% is sufficient. If they expect you to create copy and figure everything out plus they don't reply and they keep wanting changes, shoot for 20% on top of design and coding work. Responsible person —> POs
   9. Design: ask Design Lead.
  10. Coding: ask devs. **ALWAYS ADD BUFFER TO WHATEVER DEVS PROVIDE.** they always underestimate.
  11. QA manual testing: usually 1MD for complex features and 0.5MD for easier features. Responsible person —> you (if no automatic testing is required) or Spok (if automatic testing is required)
  12. QA automations: discuss if automated test is needed, if yes , ask Spok to estimate
  13. Roundup: roundup single parts of the estimation, in units of %. Then take the full number and round it up in units of % to gain buffer.
  14. Ballpark: if the project is complex, it's good to provide ballpark (a range) instead of a precise estimation. The client needs to be informed, that this is a rough estimation, and it may vary by +- 10%. Of course, it depends on the size of the project. If it's a landing page, try to be precise, as the scope is pretty small.
  15. Include timeline: clients want to know not only how much it will cost, but when it could be done. to check availability ask Vale.

### When client wants to pay for the discovery package (example: Lightverse)

* Depending on the complexity of the project, the package is priced 200.000-300.000 czk and it's approx 2months of work of a PO + Architect (for brainstorms and estimations).
* During the discovery you should gather enough information to put together a more precise estimation. Go through all the workflows to have clarity on what you should exactly scope and develop. Use the points from above.
* Do not forget that in this case the client expects a precise estimation and a clear roadmap for development which includes exact timelines.


\
Notes

* in case of client not paying for discovery, we should add to contracts that the price is not precise and we have +- 10% up and down (example EDRI)