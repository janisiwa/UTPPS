# UTPPS
Utah Private Package Service will determine the best routing for package deliveries
# Package Delivery Route Optimization

This project uses the **nearest neighbor algorithm** to create an efficient delivery route for a truck loaded with packages. It focuses on simplicity and speed, making it a good fit for small to medium delivery routes.

---

## Strengths of the Algorithm I Used

### Simple and Fast  
The nearest neighbor algorithm is easy to understand and quick to run. It looks at the closest package each time and adds it to the route. That means it doesn’t need to check every possible route, which saves time.

### Works Well for Small or Medium Routes  
This approach gives a good enough solution when you’re not dealing with hundreds of stops. It helps the driver finish deliveries faster without needing a complex system.

---

## What I’d Do Differently Next Time

If I did this project again, I’d:

- Add **package constraints**, like delivery time windows or rules for grouping certain packages together.  
- Use a **distance matrix** or cache repeated distance lookups to speed up the process, especially on longer routes.  
- Look into **other optimization techniques** that might offer better performance for larger datasets.


## Other Data Structures That Could Work

### Graph  
A graph could represent each address as a node and the distances as weighted edges. This would be a better fit for more advanced pathfinding algorithms like Dijkstra’s or A*.

### Priority Queue  
A priority queue could help me quickly find the closest next package instead of checking all packages one by one. It would make the nearest neighbor process faster.

---

### How These Are Different

- A **graph** would give me a full map-like structure that’s easier to use with complex pathfinding methods but takes more setup.  
- A **priority queue** would make it quicker to get the next best stop, but it adds some complexity compared to just looping through a list.

---

## Summary

This project met the goal of creating an efficient delivery route using a simple algorithm and straightforward data structures. It works well for the scope of the problem, and I now see how it could be extended for more advanced scenarios in the future.
