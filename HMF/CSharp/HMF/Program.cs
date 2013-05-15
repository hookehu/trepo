/**
The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**/
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;

namespace HMF
{
    class Program
    {
        static void Main(string[] args)
        {
            double a = 4.1;

            byte[] s = BitConverter.GetBytes(a);
            System.Console.WriteLine(s[0]);
            System.Console.WriteLine(s[1]);
            System.Console.WriteLine(s[2]);
            System.Console.WriteLine(s[3]);
            System.Console.WriteLine(s[4]);
            System.Console.WriteLine(s[5]);
            System.Console.WriteLine(s[6]);
            System.Console.WriteLine(s[7]);
            System.Console.WriteLine("hello world");
            Thread.Sleep(5000);
        }
    }
}
