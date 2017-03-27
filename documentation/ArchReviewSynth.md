# Architecture Review Reflection and Synthesis

Dillinger is a cloud-enabled, mobile-ready, offline-storage, AngularJS powered HTML5 Markdown editor.

**Feedback from Teaching Team:**
- The audience thinks we are approaching the project in the right direction
- We received suggestions for path planning algorithms to look into, including the traveling salesman problem and genetics algorithms.
- Suggestions for user input that can direct how the path is chosen (whether total time or number of stops is most important to each individual user). Multiple routes could be suggested based on weighting parameters differently.
- It was suggested that we look into either generating fake data for stores or scraping sites (e.g. Amazon Fresh) for data to improve the amount of data available to test our program.
- Our intuition was confirmed when we learned we will definitely need to cache data. Different possibilities were suggested, including caching searches or “caching” (reading/randomly generating) customer receipts/purchase history.

**Moving Forward:**
- We’re going to all research the traveling salesman problem (TSP).
  - Use what we learn from the TSP problem to weight components of our algorithm
- We are going to plan our User Interface to accommodate for varying levels of input from the user to personalize their experience
- We’re also going to keep in mind the idea of generating fake data for nearby stores based on what we think they should carry, in order to make our algorithm more useful, should our API not provide us with enough data.

**Overall:**
Overall the review went very well. We were able to present what we plan on doing and received guidance and direction in how to approach our problems. We are definitely ready to start creating our MVP and we now have a better idea of how to best create the algorithms for path planning. There were also great suggestions that we had not thought of on how to build on our MVP.
