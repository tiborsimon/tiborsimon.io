Title: Generating sinusoid signals
Subtitle: All possible ways to generate a sine wave
Tags: signals, basics
Date: 2015-10-17
Series: TSPR0003
Img: img/thumb-449x286-7.jpg
Summary: Generating sinusoid signals is often the first step for executing a more complex computation. It should be a routine, but actually it isn't. Many people struggles with it.
Mathjax: true


## The problem

The equation of a sinusoid signal is a known fact:

<p class="equation">
  $$y(t) = A \sin(2 \pi f t + \varphi) = A \sin(\omega t + \varphi).$$
</p>

However. This equation is only valid in the __continuous time__ domain, therefore without any modification it is useless in the __discrete time__ domain used by every digital machine. You won't be able to create a continuous variable that spans through the duration of the signal from the beginning to the end while taking up every possible value.

Machines work with _discrete time series_ that has a property called __resolution__. Resolution is the link between _continous_ and _discrete_ time domain. This property is implemented with __sampling__. It tells us how many data points were sampled equidistantly from the continuous signal within a time segment. In this way we can represent a continuous signal with discrete data points[^1].

Therefore the _t_ variable in the equation can be represented as a vector of data points. To create such a time vector, you have to choose a sampling interval.

Let's say you want to get __10 samples per seconds__ _(fs=10Hz)_, and you want to have __20 samples__ in your vector. That also means that your time vector will cover almost __2 seconds__[^2] of continuous time.

You can test that the `t1` and `t2` vector are exactly the same. Both vector starts from zero and ends at 1.9. Having the time vector we can generate a sinusoid signal with a frequency of 1Hz. This will result 2 periods in the signal:

```
s = sin(2*pi*1*t1);
```

If we plot the generated signal, we can see, that it is not a sine signal at all. It is a discrete signal, that has values in discrete points as we expected.

<img src="/images/articles/smart-sinusoids/signal001.png" alt="Discrete vs continous time sine signal" />

This method is one of the 4 main signal generation methods where we link the discrete time signal to the continuous time. Having such a connection between the two domain, the signal can be played back with the computer's _digital to analog converter_.

However. There are other use cases when we don't want to link the __discrete time__ to the __continuous time__, so we don't have to bother with the sampling frequency, and we can generate a time vector from 0 to 1, and pass it to the equation:

```
t = linspace(0,1,100);
s = sin(2*pi*3*t);
```

The result will be a 100 sample long sinusoid signal, that contains 3 periods. But be careful. This signal can't be used as the previous one until we specify the sampling frequency.

<img src="/images/articles/smart-sinusoids/signal002.png" alt="100 samples long sinusoid without discrete/continous time lock" />

As you can see, generating sinusoids with these basic methods isn't hard at all. But you __have to think__ about the method, the formulas and the units. This could be a bit time consuming if you have to think about it every time you want to generate a signal..

## Sinusoid signal parameters

There are 9 parameters that a pure sinusoid signal could have. In order to be able to generate any kind of sinusoid signals, you should be familiar with the parameters.

<img src="/images/articles/smart-sinusoids/detailed.png" alt="Sinusoid signal parameters" />


| Parameter name | Unit | Possible parameters   |
|:--------------|:----|:---------------------|
| `phi`        | [degree]    | phase          |
| `A`          | [full scale] | amplitude[^3] |
| `f`          | [Hz]   | frequency           |
| `fs`         | [Hz]  | sample rate          |
| `T`          | [s]   | period               |
| `dt`         | [s]   | sample time          |
| `L`          | [s]   | signal duration      |
| `N`          | [-]   | number of periods    |
| `n`          | [-]   | number of samples    |

With these parameters there are 5 main generation methods for sinusoid signals. Each of them have alternatives that doesn't count as an individual generation method due to the used parameters can be derived from the others if you apply the following formulas: _fs = 1/dt_, _T = 1/f_ and _L=n*dt_.

| Method index | Required parameters | CT DT lock     | Description  |
|:-------------|:------------------|:--------------|:-------------|
| 1 | `n` `N`          | No  | a signal consisting of `n` data points with `N`<br> periods in it
| 2 | `L` `N` `fs`    | Yes | `L` seconds long signal sampled at `fs` consisting of <br>`N` periods in it
| 3 | `f` `N` `fs`    | Yes | a signal sampled at `fs` sampling rate with `N` <br>periods in it with the frequency `f`
| 4 | `f` `n` `fs`    | Yes | a signal consisting of `n` <br>data points sampled at `fs` sampling rate with the frequency `f`
| 5 | `f` `L` `fs`    | Yes | a signal sampled at `fs` sampling rate with the <br>duration of `L` seconds with the frequency `f`

Let's try out all methods, to see how you can use them in practice. Let's generate the same 60 samples of sinusoid signal with 2.5 periods in it with the amplitude 1 at an arbitrary sampling frequency:

<img src="/images/articles/smart-sinusoids/demo_signal.png" alt="Reference signal for all the following generation methods" />

The used parameters may seem a bit odd for the first time, but due to the constraint of generating the same signal with all the methods, they will be reasonable.

### Method 1 - [n,N]

Generating a sinusoid signal with `n` data points with `N` periods in it.

```
n = 60;
N = 2.5;

k = 0:n-1;
k = k/n;
s = sin(2*pi*N*k);

stem(s)
```


### Method 2 - [L,N,fs]

Generating `L` seconds long signal sampled at `fs` consisting of `N` periods in it.

```
fs = 10;
N = 2.5;
L = 60/fs;

k = 0:1/fs:L-1/fs;
k=k/L;
s = sin(2*pi*N*k);

stem(s)
```


### Method 3 - [f,N,fs]

Generating a sinusoid signal sampled at `fs` sampling rate with `N` periods in it with the frequency `f`.

```
fs = 10;
N = 2.5;
f = N*fs/60;

k = 0:1/fs:(N/f)-1/fs;
s = sin(2*pi*f*k);

stem(s)
```


### Method 4 - [n,f,fs]

Generating a signal consisting of `n` data points sampled at `fs` sampling rate with the frequency `f`.

```
fs = 10;
n = 60;
f = 2.5*fs/n;

k = 0:n-1;
k = k*(1/fs);
s = sin(2*pi*f*k);

stem(s)
```


### Method 5 - [f,L,fs]

Generating a sinusoid signal sampled at `fs` sampling rate with the duration of `L` seconds with the frequency `f`.

```
L = 60/fs;
f = 2.5/L;

n = 0:1/fs:L-1/fs;
s = sin(2*pi*f*n);

stem(s)
```


## Summary

That's it. These 5 methods cover all the possible non redundant ways to generate sinusoidal signals. Did you understand them? Did you like them? Will you use them? Will you _study_ them? Will you _derive_ them over and over again?

If your answers for the last two questions were both _nope_, then the go ahead and meet <b><a href="http://tiborsimon.io/projects/#TSPR0003">Smart Sinusoids</a></b>.

[^1]: Of course this is a very high level overview of the [sampling theorem](http://en.wikipedia.org/wiki/Nyquist-Shannon_sampling_theorem). There are much more detail how these things really work.

[^2]: Because we have started our time vector from 0 as the first vector point, the remained 19 points wont cover all the 2 seconds time duration but will span until 1.9 seconds _(2s - 1/fs = 1.9s)_.

[^3]: PC sound cards usually accept signals scaled -1 to 1.
