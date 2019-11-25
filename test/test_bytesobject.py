from .support import HPyTest

class TestBytesObject(HPyTest):

    def test_Bytes_Check(self):
        mod = self.make_module("""
            HPy_DEF_METH_O(f)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                if (HPyBytes_Check(ctx, arg))
                    return HPy_Dup(ctx, ctx->h_True);
                return HPy_Dup(ctx, ctx->h_False);
            }
            @EXPORT f HPy_METH_O
            @INIT
        """)
        assert mod.f(b'hello') is True
        assert mod.f('hello') is False

    def test_Bytes_Size(self):
        mod = self.make_module("""
            HPy_DEF_METH_O(f)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                HPy_ssize_t a = HPyBytes_Size(ctx, arg);
                HPy_ssize_t b = HPyBytes_GET_SIZE(ctx, arg);
                return HPyLong_FromLong(ctx, 10*a + b);
            }
            @EXPORT f HPy_METH_O
            @INIT
        """)
        assert mod.f(b'hello') == 55

    def test_Bytes_AsString(self):
        mod = self.make_module("""
            HPy_DEF_METH_O(f)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                long res = 0;
                HPy_ssize_t n = HPyBytes_Size(ctx, arg);
                char *buf = HPyBytes_AsString(ctx, arg);
                for(int i=0; i<n; i++)
                    res = (res * 10) + buf[i];
                return HPyLong_FromLong(ctx, res);
            }
            @EXPORT f HPy_METH_O
            @INIT
        """)
        assert mod.f(b'ABC') == 100*ord('A') + 10*ord('B') + ord('C')

    def test_Bytes_AS_STRING(self):
        mod = self.make_module("""
            HPy_DEF_METH_O(f)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                long res = 0;
                HPy_ssize_t n = HPyBytes_Size(ctx, arg);
                char *buf = HPyBytes_AS_STRING(ctx, arg);
                for(int i=0; i<n; i++)
                    res = (res * 10) + buf[i];
                return HPyLong_FromLong(ctx, res);
            }
            @EXPORT f HPy_METH_O
            @INIT
        """)
        assert mod.f(b'ABC') == 100*ord('A') + 10*ord('B') + ord('C')
