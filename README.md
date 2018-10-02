# Timeflies

Handy decorator for profiling things.

## Usage

````
from timeflies import profile

@profile()
def long_running_task():
    example()

# or
with profile():
    example()
````
