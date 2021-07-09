def r_xor():
    for i in range(0,127):
        for j in range(0,127):
            result=i^j
            # print("  "+chr(i)+" ASCII:"+str(i)+' <--xor--> '+chr(j)+" ASCII:"+str(j)+' == '+chr(result)+" ASCII:"+str(result))
            if(chr(result)=='s'):
                print(str(result)+'='+chr(i)+'^'+chr(j))
                # break

if __name__ == "__main__":
    r_xor()
# ls  ('@'^',').('('^'[')