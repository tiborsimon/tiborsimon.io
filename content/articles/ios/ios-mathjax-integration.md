---
title: Local MathJax in iOS apps
tags: MathJax, ios, hack, javascript, swift, math, LaTEX
date: 2016-02-20
collection: articles
layout: article.html
summary: Integrating MathJax locally in an iOS app to be able to use mathematical equations stored in LaTEX.
---


In this article I am going to show you a method to integrate [MathJax](https://www.mathjax.org) - _an external javascript display engine for mathematics_ - in an iOS app. I used the following components:

| Component | Version |
|:-----:|:--------------------:|
| XCode | Version 7.2.1 (7C1002) |
| iOS   | 9.2                    |
| MathJax | 2.6.1                |


## Prerequisite

I wanted to display _mathematical equations_ inside an iOS app using existing math render packages. According to [this Stack overflow answer](http://stackoverflow.com/a/16002611), _mathML_ is supported by UIWebView since iOS 5. The downside of this solution, is that you have to use another packages to convert a convenient math equation reprsentation (like LaTEX) to mahtML which is very unconvenient:

```
<math title="2^(2/(sqrt(6))" xmlns="http://www.w3.org/1998/Math/MathML">
  <mstyle mathcolor="blue" fontfamily="sanserif" displaystyle="true">
    <msup>
      <mn>2</mn>
      <mrow>
        <mfrac>
          <mn>2</mn>
          <mrow>
            <msqrt>
              <mrow>
                <mn>6</mn>
              </mrow>
            </msqrt>
          </mrow>
        </mfrac>
      </mrow>
    </msup>
  </mstyle>
</math>
```

The equivalent __LaTEX__ representation is:

```
2^{\frac{2}{\sqrt{6}}}
```

To be able to use LaTEX, a third party engine is needed to produce renderable html from it. I chose [MathJax](https://www.mathjax.org) for this purpose.

## Downloading MathJax

Download the sources from <a href="https://github.com/mathjax/MathJax/releases/latest" target="_blank">MathJax's Github page</a>. At the time I wrote this article, the latest version was _2.6.1_. It could take quite a bit of time to download the whole zip file.

I put the downloaded files into the Xcode project's Vendor folder:

Simply unboxed the zip, the package takes up __180 MB__ space _(that's a lot!)_. In a future article I will show you the minimal needed content of this package that is be able to render the expressions.


<div class="gallery">
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-vendor-folder.png" alt="Location of the downloaded MathJax sources" data-jslghtbx data-jslghtbx-caption="Location of the downloaded MathJax sources" data-jslghtbx-group="mathjax-ios-group-03" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-raw-package-size.png" alt="Size of the freshly downloaded package" data-jslghtbx data-jslghtbx-caption="Size of the freshly downloaded package" data-jslghtbx-group="mathjax-ios-group-03" />
</div>

## Adding the MathJax package to the project

I added the downloaded and extracted MathJax sources to a single view based Xcode project, by dragging the folder into the project navigator. I unchecked the copy sources option.


<div class="gallery">
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/adding-the-sources.png" alt="Adding the sources to the project" data-jslghtbx data-jslghtbx-caption="Adding the sources to the project" data-jslghtbx-group="mathjax-ios-group-02" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/copy-items.png" alt="Unchecking the copy items if needed option" data-jslghtbx data-jslghtbx-caption="Unchecking the copy items if needed option" data-jslghtbx-group="mathjax-ios-group-02" />
</div>


## Using the MathJax package

After the sources are placed to the right place, it's time to use them. I draged a _UIWebView_ to the Storyboard, and created a connection to the ViewController class (`@IBOutlet weak var myWebView: UIWebView!`). I wanted to display the following simple html page in the UIWebView...

```
<!DOCTYPE html>
<html>
    <head>
        <title>MathJax TeX Test Page</title>
        <script type="text/javascript" async
            src="MathJax-2.6.1/MathJax.js?config=TeX-AMS_CHTML">
            </script>
    </head>
    <body>
        <div style="font-size: 30pt; color: #eee;">
            $$    
            \begin{equation}
              \prod_{\substack{
                        1\le i \le n\\
                        1\le j \le m}}
                 M_{i,j}
            \end{equation}
            $$
        </div>
    </body>
</html>
```
... so I used its `loadHTMLString` method to do that:

```
//
//  ViewController.swift
//  MathJaxTest01
//
//  Created by Tibor Simon on 20/02/16.
//  Copyright © 2016 Tibor Simon. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var myWebView: UIWebView!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.

        let path = NSBundle.mainBundle().bundlePath
        let baseURL = NSURL.fileURLWithPath(path)

        let myHTML = "<!DOCTYPE html><html><head><title>MathJax TeX Test Page</title><script type=\"text/javascript\" async  src=\"MathJax-2.6.1/MathJax.js?config=TeX-AMS_CHTML\"></script></head><body>  <div style=\"font-size: 30pt; color: #eee;\">$$\\begin{equation}\\prod_{\\substack{1\\le i \\le n\\\\ 1\\le j \\le m}}M_{i,j} \\end{equation}$$</div></body></html>"
        myWebView.loadHTMLString(myHTML, baseURL:baseURL)

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}

```

## Testing with the simulator

The project loads up to the simulator a bit slowly. After it loads, it renders the mathematical expression to the _UIWebView_ in 8 phases:

<div class="gallery">
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-00.png" alt="Rendering phase 1: It starts as a blank screen." data-jslghtbx data-jslghtbx-caption="Rendering phase 1: It starts as a blank screen." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-01.png" alt="Rendering phase 2: Then it loads the raw LaTEX source." data-jslghtbx data-jslghtbx-caption="Rendering phase 2: Then it loads the raw LaTEX source." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-02.png" alt="Rendering phase 3: First rendering pass." data-jslghtbx data-jslghtbx-caption="Rendering phase 3: First rendering pass." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-03.png" alt="Rendering phase 4: Loading CommonHTML sources for the final rendering pass." data-jslghtbx data-jslghtbx-caption="Rendering phase 4: Loading CommonHTML sources for the final rendering pass." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-04.png" alt="Rendering phase 5: Renders final image." data-jslghtbx data-jslghtbx-caption="Rendering phase 5: Renders final image." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-05.png" alt="Rendering phase 6: Becames blank again." data-jslghtbx data-jslghtbx-caption="Rendering phase 6: Becames blank again." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-06.png" alt="Rendering phase 7: Final image appears in fractions." data-jslghtbx data-jslghtbx-caption="Rendering phase 7: Final image appears in fractions." data-jslghtbx-group="mathjax-ios-group" />
  <img class="jslghtbx-thmb" src="/images/articles/mathjax-ios/mathjax-ios-07.png" alt="Rendering phase 8: Render finished." data-jslghtbx data-jslghtbx-caption="Rendering phase 8: Render finished." data-jslghtbx-group="mathjax-ios-group" />
</div>

The whole rendering happens in less then half a second, but it is noticeable. If you want to use this method to render mathematical expresions in your app, you have to make sure, you only show your _UIWebView_, when it fulli loaded.

## Try it out yourself!

You can download the whole Xcode project with the added MathJax sources from <a href="https://github.com/tiborsimon/ios-local-mathjax-template" target="_blank">the project's Github repository</a>.

## Acknowledgement

For this project, I get a lot of ideas from <a href="http://new2objectivec.blogspot.hu/2013/03/mathjax-v21-works-beautifully-on-ios-61.html?m=1" target="_blank">New 2 Objective-C</a> blog. His implementation is based on a local file writing and reading, which is pretty slow, but it works :)

I also used some ideas from Stack Overflow to <a href="http://stackoverflow.com/questions/3646930/how-to-make-a-transparent-uiwebview" target="_blank">make my UIWebView transparent</a>
