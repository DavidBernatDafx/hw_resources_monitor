HW resources monitor. -

It was created as my challenge in 15-20 hours of coding, and exploring possible solutions in limited time.
Comap HW resources monitor is a simple turbo-flask webapp, that is displaying CPU, RAM, Drive, and Net usage and updates
data in HTML document every 5 seconds.

The biggest challenge was how to include matplotlib and seaborn figures via jinja2 into HTML document.
It is still work in progress, there are needed various mpl styling tweaks, adding axes ticks, and general css/bootstrap
optimizations.
But the backend is runnig with no issues and bugs, and this was the primary goal I wanted to achieve in limited time.