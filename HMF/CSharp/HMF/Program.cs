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
using System.IO;
using System.Timers;

namespace HMF
{
    class Program
    {
        static void Main(string[] args)
        {
            using (FileStream fd = File.OpenRead("E:\\out.hmf"))
            {
                System.Console.WriteLine(fd.Position);
                int len = (int)fd.Length;
                byte[] bs = new byte[len];
                fd.Read(bs, 0, len);
                System.Console.WriteLine("eee " + bs[0]);

                Hmf h = new Hmf();
                MemoryStream st = new MemoryStream(bs);
                st.Seek(0, SeekOrigin.Begin);
                System.Console.WriteLine(st.Position);
                System.Console.WriteLine(DateTime.Now.Second + "   " + DateTime.Now.Millisecond);
                Dictionary<object, object> d = (Dictionary<object, object>)h.ReadObject(st);
                System.Console.WriteLine(d.Count);
                System.Console.WriteLine(DateTime.Now.Second + "   " + DateTime.Now.Millisecond);
            }
            System.Console.WriteLine("hello world");
            Thread.Sleep(10000);
        }
    }
}
