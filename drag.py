def is_web():
    return "__BRYTHON__" in globals()

def write(message, end='\n'):
    if is_web():
        from browser import document
        console = document.getElementById('console')
        p = document.createElement('p')
        p.textContent = '> ' + message
        console.appendChild(p)
        console.scrollTop = console.scrollHeight
    else:
        write(message, end=end)


async def read():
    if is_web():
        from browser import document, aio
        inp = document.getElementById('input')
        while True:
            event = await aio.event(inp, 'keydown')
            if event.key == 'Enter':
                tmp = event.target.value
                event.target.value = ''
                write(tmp)
                return tmp
    else:
        return input()


def run(function):
    if is_web():
        from browser import aio
        aio.run(function())
    else:
        import asyncio
        asyncio.run(function())

def createTab(colvo):
    res = ""
    for i in range(colvo):
        res += " "
    return res

def gg(num):
    return str(num)
async def main(isStart):
    P = [0]*2; E = [0]*2; W = [0]*2; S = [0]*2; X = [0]*2; M = [0]*2
    C = [0]*2; B = [0]*2; Y = [0]*2; Q = [0]*2; D = [0]*2
    if(isStart):
        write(createTab(27) + 'DRAG')
        write(createTab(20) + 'CREATIVE COMPUTING')
        write(createTab(19) + 'MORRISTOWN NEW JERSEY')
        write('\n\n')
        write('WELCOME TO DRAG STRIP.')
        write('WOULD YOU LIKE THE INSTRUCTIONS ')
        I = await read()

        if(I != "NO"):
            write('YOU MAY RACE AGAINST ONE OF YOUR FRIENDS OR YOU MAY RACE')
            write('AGAINST MY DRAGSTER. YOU WILL BE ASKED TO DESIGN YOUR')
            write('OWN MACHINE, SPECIFYING HOURSEPOWER, READ END RATIO (X:1),')
            write('TIRE WIDTH IN INCHES AND TIRE DIAMETER IN FEET.')
    write('DO YOU WANT TO RACE AGAINST ME ')
    I = await read()

    if(I != "NO"):
        write('I WILL HAVE CAR #1.')
        P[0]=600
        E[0]=5.9
        W[0]=22
        D[0]=3.9
    else:
        write('DESIGN CAR #1:')
        write('HOURSPOWER=')
        P[0] = await read()
        P[0] = int(P[0])
        write('REAR END RATIO=')
        E[0] = await read()
        E[0] = int(E[0])
        write('TIRE WIDTH*')
        W[0] = await read()
        W[0] = int(W[0])
        write('TIRE DIAMETER=')
        D[0] = await read()
        D[0] = int(D[0])

    write('DESIGN CAR #2:')
    write('HOURSPOWER=')
    P[1] = await read()
    P[1] = int(P[1])
    write('REAR END RATIO=')
    E[1] = await read()
    E[1] = int(E[1])
    write('TIRE WIDTH*')
    W[1] = await read()
    W[1] = int(W[1])
    write('TIRE DIAMETER=')
    D[1] = await read()
    D[1] = int(D[1])
    write('\nGO!')

    K1=500
    K2=1.6
    K3=2
    K4=6e-04
    K5= 6e-05
    K6=0.2
    K7=4
    K8=1.5e-04
    Q[0]=0; Q[1]=0
    S[0]=0; S[1]=0
    X[0]=0; X[1]=0
    #M IS MASS
    for J in range(2):
        M[J] = (K1+K2*P[J]+K3*W[J]*D[J]+K7*D[J]**2)/32.2
        #C IS DRAG FROM WIND.
        C[J]=K4*M[J]**(2/3)+K8*W[J]*D[J]
        #B IS THE MAX ACCELERATION WITHOUT BURNING
        B[J]=15+28*W[J]*D[J]/((W[J]+6)*(D[J]+1))
        #Y IS THE SCALE FACTOR FOR RPN VS POUER.
        Y[J]=3.7-3.3e-03*P[J]

    write('\n')
    write('ELAPSED ' + createTab(15-8) + 'CAR #1' + createTab(39-21) + "CAR #2")
    write('TIME   SPEED     DISTANCE     SPEED     DISTANCE')
    write('(SEC)  (MPH)      (FT)        (MPH)        (FT)')
    write('')
    for T in range(100):
        for T1 in range(100):
            for J in range(2):
                #R IS RPM.
                R=60*S[J]*E[J]/(3.1415926*D[J])
                #L0 IS ENGINE TORQUE.
                L0=(P[J]/42.5)*(50+7.8e-03*(R/Y[J])-4e-10*(R/Y[J])**3)
                #L1 IS TORQUE FROM FRICTION.
                L1=P[J]*(K5*R+K6)
                #R2 IS REAR AXLE TORQUE.
                L2=E[J]*(L0-L1)
                #F IS FORCE ON ROAD FROM TIRES.
                F=2*L2/D[J]
                #TEST FOR BURN.
                if not (F > M[J]+B[J]):
                    #A=ACCELERATION
                    if not (Q[J] != 0):
                        write('CAR # ' + str(J+1) + "  STOPS BURNING RUBBER")
                        Q[J] = 1
                    A=(F-C[J]*S[J]**2)/M[J]
                else:
                    A=B[J]-C[J]*S[J]**2/M[J]
                    #S IS FEET IN FT/SEC.
                S[J]=S[J]+A*0.01
                #X IS DISTANCE IN FT.
                X[J]=X[J]+S[J]*0.01
        #TEST FOR FINISH.
            if not (X[0]<5280/4 and X[1]<5280/4):
                if not (X[0]>X[1]):
                    T3=(X[1]-5280/4)/S[1]
                    T=T+T1/100-T3
                    X[1]=5280/4
                    X[0]=X[0]-S[0]*T3
                    write(" " + str(T) + "     " + gg(S[0]*3600/5280) + "    " + gg(X[0]) + 
                          "   " + gg(S[1]*3600/5280) + "   " + gg(X[1]))
                    #write(str(S[1]*3600/5280) + "   " + str(X[1]))
                    write(createTab(40) + "WINNER")
                    write()
                    write("DO YOU WANT TO TRY AGAIN ")
                    I = await read()
                    if (I != 'YES'):
                        return False
                    else:
                        return True
                T3=(X[0]-5280/4)/S[0]
                T=T+T1/100-T3
                X[0]=5280/4
                X[1]=X[1]-S[1]*T3
                write(" " + str(T) + "     " + gg(S[0]*3600/5280) + "     " + gg(X[0])
                      + "   " + gg(S[1]*3600/5280) + "   " + gg(X[1]))
                #write(str(S[1]*3600/5280) + "   " + str(X[1]))
                write(createTab(10) + "WINNER")
                write('DO YOU WANT TO TRY AGAIN ')
                I = await read()
                if (I != 'YES'):
                    return False
                else:
                    return True
        write(" " + str(T+1) + "     " + gg(S[0]*3600/5280) + "     " + gg(X[0]) +
              "   " + gg(S[1]*3600/5280) + "   " + gg(X[1]))
        #write(str(S[1]*3600/5280) + "   " + str(X[1]))


async def game():
    bb = False
    while(True):
        res = None
        if not bb:
            res = await main(True)
        else:
            res = await main(False)
        if(not res):
            break
        bb = True

run(game)