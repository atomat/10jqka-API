import frida

import frida, sys

rdev = frida.get_remote_device()
session = rdev.attach("com.hexin.plat.android")

f = open('D:\\workplace\\frida\\log.txt',mode='wb')
f.write(b'')
f.close()

f = open('D:\\workplace\\frida\\log.txt',mode='a',encoding='utf-8')

script = session.create_script("""

    console.log("[*] Starting script");

    Java.perform(function(){
        
        //bytes2hex
        function bytes2hex(bytes) {
            for (var hex = [], i = 0; i < bytes.length; i++) { hex.push(((bytes[i] >>> 4) & 0xF).toString(16).toUpperCase());
                hex.push((bytes[i] & 0xF).toString(16).toUpperCase());
                hex.push(" ");
            }
            return hex.join("");
        }
        

        //log
        var frr = Java.use('frr');
        frr.a.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            send(arg1 + " : " + arg2);
        };
        frr.b.implementation = function (arg1, arg2) {
            send(arg1 + " bbb: " + arg2);
        };
        frr.c.implementation = function (arg1, arg2) {
            send(arg1 + " : " + arg2);
        };
        frr.d.implementation = function (arg1, arg2) {
            send(arg1 + " : " + arg2);
        };
        frr.e.implementation = function (arg1, arg2) {
            send(arg1 + " : " + arg2);
        };
        
        var frq = Java.use('frq');
        frq.a.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            this.a(arg1, arg2);
            send(arg1 + " : " + arg2);
        };
        frq.a.overload('java.lang.String', 'java.lang.String', 'boolean').implementation = function (arg1, arg2, arg3) {
            this.a(arg1, arg2, arg3);
            send(arg1 + " : " + arg2);
        };
        frq.b.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            this.b(arg1, arg2);
            send(arg1 + " : " + arg2);
        };
        frq.c.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            this.c(arg1, arg2);
            send(arg1 + " : " + arg2);
        };
        frq.d.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            this.d(arg1, arg2);
            send(arg1 + " : " + arg2);
        };
        frq.e.overload('java.lang.String', 'java.lang.String').implementation = function (arg1, arg2) {
            this.e(arg1, arg2);
            send(arg1 + " : " + arg2);
        };
        
        //uncompress
        var snapcompress = Java.use('org.xerial.snappy.Snappy');
        snapcompress.uncompress.overload('[B', 'int', 'int', '[B', 'int').implementation = function(arg1, arg2, arg3, arg4, arg5){
            send('compress:' + bytes2hex(arg1));
            var ret = this.uncompress.overload('[B', 'int', 'int', '[B', 'int').apply(this, arguments);
            send('uncompress:' + bytes2hex(arg4));
            return ret;
        }
        
        //nativeDES
        var SecurityModule = Java.use('com.hexin.android.security.SecurityModule');
        SecurityModule.decrypt3DES.overload('[B', '[B').implementation = function(arg1, arg2){
            var ret = this.decrypt3DES(arg1, arg2);
            send('nativeDES_dkey:' + bytes2hex(arg1));
            send('nativeDES_dcipher:' + bytes2hex(arg2));
            send('nativeDES_dplain:' + bytes2hex(ret));
            return ret;
        }
        SecurityModule.encrypt3DES.overload('[B', '[B').implementation = function(arg1, arg2){
            var ret = this.encrypt3DES(arg1, arg2);
            send('nativeDES_ekey:' + bytes2hex(arg1));
            send('nativeDES_eplain:' + bytes2hex(arg2));
            send('nativeDES_ecipher:' + bytes2hex(ret));
            return ret;
        }
        
        //javaDES
        var fhy = Java.use('fhy');
        fhy.a.overload('[B', 'int', 'int', 'boolean').implementation = function(arg1, arg2, arg3, arg4){
            if(arg4){
                send('javaDES1_plain:' + bytes2hex(arg1));
                this.a(arg1, arg2, arg3, arg4);
                send('javaDES1_cipher:' + bytes2hex(arg1));
            }else{
                send('javaDES1_cipher:' + bytes2hex(arg1));
                this.a(arg1, arg2, arg3, arg4);
                send('javaDES1_plain:' + bytes2hex(arg1));
            }
        }
        fhy.a.overload('[B', 'int', 'boolean').implementation = function(arg1, arg2, arg3){
            if(arg3){
                send('javaDES2_plain:' + bytes2hex(arg1));
                this.a(arg1, arg2, arg3);
                send('javaDES2_cipher:' + bytes2hex(arg1));
            }else{
                send('javaDES2_cipher:' + bytes2hex(arg1));
                this.a(arg1, arg2, arg3);
                send('javaDES2_plain:' + bytes2hex(arg1));
            }
        }
        /*
        //RSA加密部分
        var bitInt = Java.use('java.math.BigInteger');
        bitInt.modPow.implementation = function(arg1, arg2){
            send('BigInteger');
            v1 = this.toByteArray();
            v2 = arg1.toByteArray();
            v3 = arg2.toByteArray();
            send('BigInteger_p1:' + bytes2hex(v1));
            send('BigInteger_p2:' + bytes2hex(v2));
            send('BigInteger_p3:' + bytes2hex(v3));
            ret = this.modPow(arg1, arg2);
            r1 = ret.toByteArray();
            send('BigInteger_p3:' + bytes2hex(r1));
            return ret;
        }
        */
    });
""")


def on_message(message, data):
    if message['type'] == 'error':
        print(message['stack'])
    elif message['type'] == 'send':
        print(message['payload'])
        f.write(message['payload'] + '\n')
        f.flush()
    else:
        print(message)


script.on('message', on_message)
script.load()
# rdev.resume(pid);
sys.stdin.read()