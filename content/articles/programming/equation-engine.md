Title: Writing an equation engine
Subtitle: Finding out the possibilities programmatically
Tags: parameter, equation
Date: 2015-11-11
Series: TSPR0003
Summary: In the previous article we have discussed the 5 ways you can generate a sinusoid signal. In this article we are going to develop a method that tries to generate a sinusoid signal with a given parameter set.


## Sinusoid generation summary

Let's sum up the previous article. If you want to generate a sinusoid signal you have 5 possibble ways to do that.

| Method index | Required parameters | Description  |
|:-------------|:--------------|:-------------|
| 1 | `n` `N`          | a signal consisting of `n` data points with `N`<br> periods in it
| 2 | `L` `N` `fs`    | `L` seconds long signal sampled at `fs` consisting of <br>`N` periods in it
| 3 | `f` `N` `fs`    | a signal sampled at `fs` sampling rate with `N` <br>periods in it with the frequency `f`
| 4 | `f` `n` `fs`    | a signal consisting of `n` <br>data points sampled at `fs` sampling rate with the frequency `f`
| 5 | `f` `L` `fs`    | a signal sampled at `fs` sampling rate with the <br>duration of `L` seconds with the frequency `f`

Where the parameters are

| Parameter | Unit | Parameter name   |
|:--------------|:----|:---------------------|
| `phi`        | [degree]    | phase          |
| `A`          | [full scale] | amplitude |
| `f`          | [Hz]   | frequency           |
| `fs`         | [Hz]  | sample rate          |
| `T`          | [s]   | period               |
| `dt`         | [s]   | sample time          |
| `L`          | [s]   | signal duration      |
| `N`          | [-]   | number of periods    |
| `n`          | [-]   | number of samples    |

## Required parts

To create an equation engine we have to solve the following problems:

1. Identify the passed parameters
1. Calculate the necessary parameters from the available ones
1. Use the parameters in the equations

### Identifying the passed parameters

We need to identify what parameters were passed to the generator function to be able to decide what parameters can we
calculate with the passed ones. Hopefully we can use <a href="http://tiborsimon.io/projects/TSPR0002/" target="_blank">Simple Input Parser</a>
that can provide the passed parameter flags in its _extra flag_ mode.

<div data-gist-id="63262ac34b22694c617d" data-gist-file="input_parsing.m"></div>

The flags variable will be the structure that will contain the parameter flags. One if the parameter was parsed and
zero if not.

### Calculating the parameters

To be able to substitute to the generator equations, we need to make sure to have all the necessary parameters
to do that. In case if wo do not have all the ones, we have to try to calculate them from the given ones.

The following table contains all possible way to get a parameter from the others.

| f   | T   | n   | N   | fs  | dt  | L   |
|:---|:---|:---|:---|:---|:---|:---|
| 1/T | 1/f | L fs | L/T | 1/dt | 1/fs | N T |
| N/L | L/N | L/dt | L f | n/L | L/n | n dt |
| n dt/L/T | L/n/dt/f | N T/dt | n dt/T | n/N/T | N T/n | N/f |
| n/fs/T/L | L fs/n/f | N T fs | n dt f | n/L/f/T | L f T/n | n/fs |
| - | - | - | n/fs/T | - | - | - |
| - | - | - | n f/fs | - | - | - |

This table can be programmed into __calculator functions__ which are going to try to calculate a parameter from the
others. If a _calculator function_ is unable to calculate a parameter it throws an exception.

<div data-gist-id="63262ac34b22694c617d" data-gist-file="parameter_calculators.m"></div>

### Using the parameters in the equations

Lastly we have to implement the __generator functions__ for all 5 cases. These functions implement the
sinusoid signal generation with a given parameter set. For more details see the first episode of this article series.

<div data-gist-id="63262ac34b22694c617d" data-gist-file="generator_functions.m"></div>

## Putting everything together

The last step is to put everything together.

1. We have the flag structure that indicates what parameters were passed. This structure can be used by the _calculator functions_ to
   determine if a parameter can be calculated or not.
1. We have _calculator functions_ that can calculate the necessary parameters for the _generator functions_. If one parameter cannot be
   calculated, an exception will be raised.
1. We have _generator functions_ that can generate the sinusoid signal if all necessary parameters are available for them.

The only thing what we have to do is to use the _generator functions_ to try to generate the sinusoid signal in __every possible way__.
If one _generator function_ fails, we try another until there is no more _generator function_ left. In that case we can determine, that
the given parameter set, there is no way to generate a sinusoud signal.

<div data-gist-id="63262ac34b22694c617d" data-gist-file="equation_selection.m"></div>

## Summary

And that's it. This method was used in <a href="http://tiborsimon.io/projects/TSPR0003/" target="_blank">Smart Sinusoids</a> to generate
the sinusoid signals.
