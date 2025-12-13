class A {
    B x;

    long myMethod(B a, A[] b) {
        int k = 0;
        b[k].x = a;
        B.y = B.y + 3;
        return B.y;
    }
}

class B extends A {
    static long y;

    long myMethod(A[] a) {
        y = y + 1;
        return myMethod(this, a);
    }
}