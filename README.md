I read an [article]([url](https://nautil.us/how-to-solve-the-drone-traffic-problem-779798/)) about using the ideas around how birds fly in flocks to help with drone congestion.

This is a really interesting idea: If the drone is semi autonomous it needs to be able to make a "smart" decision probably faster than a human (or centralized control system) could.

I decided to explore this problem with some help from claude.ai, so I described the problem and let it produce the framework.

## Why?
I have some questions and this project is here to help me answer them.

- [x] What does a "simple" simulation look like in python?
  - I play around with spreadsheets all the time, what does something more time-based look like?
  - I don't need a pro-level framework, just something simple that can be added to if needed.
  - Success! This code is pretty straightforward. Even the drawing code seems to make sense at first glance. Modifications haven't been an issue.
- [x] Can an LLM (claude.ai in this case) be a good partner to learn these things?
  - A good back-and-forth as I learn more about the domain and simulation in general
  - Calling this success! I was able to quickly communicate what I wanted or wanted changed and we were able to produce something working and interesting quickly.
- [ ] Flocking behavior in general
  - What do the emergent travel lanes look like?
  - If an emergent lane is disrupted, how does the system adapt (and how quickly)?
- [ ] Thinking about how drones could work in a congested environment
  - Drone delivery is a great idea, but there will be issues with traffic around the "base". It would be best if the drones could solves this amongst themselves.
  - What about other considerations like noise, or "restricted" areas (playgrounds, hospitals)?

