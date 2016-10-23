#IMPORTANT!
This is only for development, this makes your code may make your 
project vulnerable.

# DjangoRandom
Create Random Data For Models -- Without having to modify existing models.


# Info on Usage
- Multiple populations can be generated for each model
- Multiple samples can be generated for each model
- Can reference a single population for testing (without creating a sample)
- Can specify non-probabilistic distribution for boolean field on a population. You can do this by stating the percentage of true or false (field values are in UPPERCASE).

## DISTRIBUTION Option
the percentage of the population size that should be generated

## Random Option

## Ensure Distribution
ensure that a choice is made a certain percentage of time. This means that if we
generate n boolean choices with 50% true, that even though selection is random, 
the percentage of true in the population is 50%.

## SPEC option
the spec option is meant to provide a means of specifying a value for part of 
the distribution or of getting a value, or set of values, for part of the 
distribution

#TODO
###Add filters to ForeignKey Choice Distribution value
###Add Name to Choice Distribution
###In Discussion: Change choice distribution value to accept django code
We could modify value to parse code into python code and validate it as
a function or generator for providing values. This would make the code 
extra vulnerable, but this project should never be included in production.
