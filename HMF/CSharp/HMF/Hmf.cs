/**
The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**/
using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace HMF
{
    class Hmf
    {
        private List<uint> ints = new List<uint>();
        private List<double> doubles = new List<double>();
        private List<bool> bools = new List<bool>();
        private List<string> strs = new List<string>();

        private Stream stream = new MemoryStream();

        public Hmf()
        {
        }

        public void Reset()
        {
            ints = new List<uint>();
            doubles = new List<double>();
            strs = new List<string>();
            bools = new List<bool>();
            bools.Add(false);
            bools.Add(true);
            stream = new MemoryStream();
        }

        public void WriteObject(object obj)
        {

        }

        private void WriteInt(int v)
        {

        }

        private void WriteDouble(long v)
        {

        }

        private void WriteString(string v)
        {

        }

        private void WriteArray(List<object> v)
        {

        }

        private void WriteDict(Dictionary<object, object> v)
        {

        }

        private void MergeAll()
        {

        }

        public object ReadObject()
        {
            return null;
        }

        private void InitPool()
        {

        }

        private List<object> ReadArray()
        {
            return null;
        }

        private Dictionary<object, object> ReadDict()
        {
            return null;
        }
    }
}
