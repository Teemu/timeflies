# Timeflies

Simple decorator for quick profiling of Python code. Also tracks SQLAlchemy queries.

![](https://i.imgur.com/17lVBAx.png)

## Usage

````python
from timeflies import profile

# Decorator usage
@profile()
def long_running_task():
    example()

# With statement
with profile():
    example()
````

## Arguments

````python

profile(
    engine=None # SQLAlchemy engine where we track how long queries take. If set to None, Timeflies tries to get the engine from Flask-SQLAlchemy.
    smart=True, # By default Timeflies tries to be smart by hooking into Flask-SQLAlchemy and hiding lines from output that don't matter.
    n=20, # How many lines to show by default. Note that if you have *smart* enabled, some of the lines will be hidden.
)

````
