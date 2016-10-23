---
title: Writing an equation engine
tags: parameter, equation
date: 2015-11-11
collection: articles
layout: article.html
summary: In the previous article we have discussed the 5 ways you can generate a sinusoid signal. In this article we are going to develop a method that tries to generate a sinusoid signal with a given parameter set.
---


# Sinusoid generation summary

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

# Required parts

To create an equation engine we have to solve the following problems:

1. Identify the passed parameters
1. Calculate the necessary parameters from the available ones
1. Use the parameters in the equations

# Identifying the passed parameters

We need to identify what parameters were passed to the generator function to be able to decide what parameters can we
calculate with the passed ones. Hopefully we can use <a href="http://tiborsimon.io/projects/TSPR0002/" target="_blank">Simple Input Parser</a>
that can provide the passed parameter flags in its _extra flag_ mode.

``` matlab
[data, flags] = simple_input_parser(data, raw_varargin, validators);
```

The flags variable will be the structure that will contain the parameter flags. One if the parameter was parsed and
zero if not.

## Calculating the parameters

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

``` matlab
%% Parameter construction
function f = get_f()
    if flags.f
        f = data.f;
    elseif flags.T
        f = 1 / data.T;
    elseif flags.N && flags.L
        f = data.N / data.L;
    elseif flags.n && flags.dt && flags.L && flags.T
        f = data.n * data.dt / data.L / data.T;
    elseif flags.n && flags.fs && flags.L && flags.T
        f = data.n / data.fs / data.L / data.T;
    else
        throw('.');
    end
end

function T = get_T()
    if flags.T
        T = data.T;
    elseif flags.f
        T = 1 / data.f;
    elseif flags.L && flags.N
        T = data.L / data.N;
    elseif flags.L && flags.n && flags.dt && flags.f
        T = data.L / data.n / data.dt / data.f;
    elseif falgs.L && flags.n && flags.fs && flags.f
        T = data.L * data.fs / data.n / data.f;
    else
        throw('.');
    end
end

function n = get_n()
    if flags.n
        n = data.n;
    elseif flags.L && flags.fs
        n = data.L * data.fs;
    elseif flags.L && flags.dt
        n = data.L / data.dt;
    elseif flags.N && flags.T && flags.dt
        n = data.N * data.T / data.dt;
    elseif flags.N && flags.T && flags.fs
        n = data.N * data.T * data.fs;
    else
        throw('.')
    end
end

function N = get_N()
    if flags.N
        N = data.N;
    elseif flags.L && flags.T
        N = data.L / data.T;
    elseif flags.L && flags.f
        N = data.L * data.f;
    elseif flags.n && flags.dt && flags.T
        N = data.n * data.dt / data.T;
    elseif flags.n && flags.dt && flags.f
        N = data.n * data.dt * data.f;
    elseif flags.n && flags.fs && flags.T
        N = data.n / data.fs / data.T;
    elseif flags.n && flags.f && flags.fs
        N = data.n * data.f / data.fs;
    else
        throw('.')
    end
end

function fs = get_fs()
    if flags.fs
        fs = data.fs;
    elseif flags.dt
        fs = 1 / data.dt;
    elseif flags.n && flags.L
        fs = data.n / data.L;
    elseif flags.n && flags.N && flags.T
        fs = data.n / data.N / data.T;
    elseif flags.n && flags.L && flags.f && flags.T
        fs = data.n / data.L / data.f / data.T;
    else
        throw('.');
    end
end

function dt = get_dt()
    if flags.dt
        dt = data.dt;
    elseif flags.fs
        dt = 1 / data.fs;
    elseif flags.L && flags.n
        dt = data.L / data.n;
    elseif flags.N && flags.T && flags.n
        dt = data.N * data.T / data.n;
    elseif flags.L && flags.f && flags.T && flags.n
        dt = data.L * data.f * data.T / data.n;
    else
        throw('.');
    end
end

function L = get_L()
    if flags.L
        L = data.L;
    elseif flags.N && flags.T
        L = data.N * data.T;
    elseif flags.n && flags.dt
        L = data.n * data.dt;
    elseif flags.N && flags.f
        L = data.N / data.f;
    elseif flags.n && flags.fs
        L = data.n / data.fs;
    else
        throw('.');
    end
end
```

## Using the parameters in the equations

Lastly we have to implement the __generator functions__ for all 5 cases. These functions implement the
sinusoid signal generation with a given parameter set. For more details see the first episode of this article series.

``` matlab
%% Signal synthesizer functions
function s = construct_with_n_N()
    n = get_n();
    N = get_N();
    phi = data.phi;

    k = 0:n-1;
    k = k/n;
    phi = phi*pi/180;
    s = trigfun(2*pi*N*k + phi);
end

function s = construct_with_L_N_fs()
    L = get_L();
    N = get_N();
    fs = get_fs();
    phi = data.phi;

    k = 0:1/fs:L-1/fs;
    k=k/L;
    phi = phi*pi/180;
    s = trigfun(2*pi*N*k + phi);
end

function s = construct_with_f_N_fs()
    f = get_f();
    N = get_N();
    fs = get_fs();
    phi = data.phi;

    k = 0:1/fs:(N/f)-1/fs;
    phi = phi*pi/180;
    s = trigfun(2*pi*f*k + phi);
end

function s = construct_with_n_f_fs()
    n = get_n();
    f = get_f();
    fs = get_fs();
    phi = data.phi;

    k = 0:n-1;
    k = k*(1/fs);
    phi = phi*pi/180;
    s = trigfun(2*pi*f*k + phi);
end

function s = construct_with_L_f_fs()
    L = get_L();
    f = get_f();
    fs = get_fs();
    phi = data.phi;

    n = 0:1/fs:L-1/fs;
    phi = phi*pi/180;
    s = trigfun(2*pi*f*n + phi);
end
```

# Putting everything together

The last step is to put everything together.

1. We have the flag structure that indicates what parameters were passed. This structure can be used by the _calculator functions_ to
   determine if a parameter can be calculated or not.
1. We have _calculator functions_ that can calculate the necessary parameters for the _generator functions_. If one parameter cannot be
   calculated, an exception will be raised.
1. We have _generator functions_ that can generate the sinusoid signal if all necessary parameters are available for them.

The only thing what we have to do is to use the _generator functions_ to try to generate the sinusoid signal in __every possible way__.
If one _generator function_ fails, we try another until there is no more _generator function_ left. In that case we can determine, that
the given parameter set, there is no way to generate a sinusoud signal.

``` matlab
%% Mode Selection
try
    s = construct_with_n_N();
catch
   try
       s = construct_with_L_N_fs();
   catch
      try
          s = construct_with_f_N_fs();
      catch
          try
              s = construct_with_n_f_fs();
          catch
              try
                  s = construct_with_L_f_fs();
              catch
                  throw_exception('parameterError','With the given parameters there is no way to construct a sinusoid signal!');
              end
          end

      end
   end
end
```

# Summary

And that's it. This method was used in <a href="http://tiborsimon.io/projects/TSPR0003/" target="_blank">Smart Sinusoids</a> to generate
the sinusoid signals.

