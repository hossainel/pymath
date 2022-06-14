#!python3 env
#@author hossainel
class Matrix:
    MArr = [[]]
    def __init__(self, M=[[]]):
        '''
For an empty Matrix
>>> A = Matrix()
Or you can call a matrix by inserting a two dimensional list
>>> A = Matrix([[2,3],
                [4,5]])
For a Zero metrix
>>> A = Matrix("Z 3 3")
For an Identity Matirx
>>> A = Matrix("I 3")
        '''
        super().__init__()
        if "str" in str(type(M)):
            k = M.split(' ')
            if k[0].upper()=='I': self.__I(int(k[1]))
            if k[0].upper()=='Z': self.__Zero(int(k[1]),int(k[2]))
            if k[0].upper()=='C': self.cramer(k)
        else: self.MArr = M
        
    def pMatrix(self):
        '''
Prints the matrix and returns None
>>> Matrix([[1]]).pMatrix()
        '''
        t=""
        for i in self.MArr:
            t=t+"|\t"
            for j in i[:-1]:
                t=t+str(j)+"\t"
            t=t+str(i[-1])+"\t|\n\n"
        self.sMArr = t
        print(t)

    def __copy(self): return [i for i in self.MArr]
            
    @property
    def row(self): return len(self.MArr)
    
    @property
    def col(self): return len(self.MArr[0])
    
    @property
    def isValid(self):
        """
Return if the valid information in boolean
>>> Matrix([[1]]).isValid
        """
        for i in self.MArr:
            if not (len(i)==self.col):
                return False
        return True
    
    @property
    def numCell(self): return self.row*self.col
    
    @property
    def __mType(self):
        if self.row == 1: return "Row"
        elif self.col == 1: return "Column"
        elif self.row==self.col: return "Square"
        else: return "Rectangular"
    
    @property
    def principalDiagonal(self): return [self.MArr[i][i] for i in range(self.col)]
    
    @property
    def trace(self): return sum(self.principalDiagonal)
    
    def transpose(self, M=[[]]):
        '''
The transpose matrix returns a Matirx class
if A is a Matrix, then its transpose will be
>>> B = A.trasnopse()
        '''
        tmp = []
        if M==[[]]:
            for i in range(self.col):
                tmp.append([self.MArr[j][i] for j in range(self.row)])
        else:
            for i in range(self.col):
                tmp.append([M[j][i] for j in range(self.row)])
            return tmp
        self.__transpose = tmp
        return Matrix(tmp)

    def mType(self):
        '''
Returns the matrix type in a list.
>>> M = Matrix()
>>> M.mType()
        '''
        if self.__mType=="Square":
            tmp = [self.__mType]
            uT = lT = slr = True
            for i in range(self.row):
                for j in range(self.col):
                    if (not self.MArr[i][j]==0):
                        if i>j: uT = False
                        if i<j: lT = False
                    if (not self.MArr[i][j]==self.MArr[0][0]) and i==j: slr = False
            if uT and (not lT): tmp.append("UpperTringular")
            if lT and (not uT): tmp.append("LowerTringular")
            if uT and lT and (not slr): tmp.append("Diagonal")
            if slr and uT and lT:
                if (not self.MArr[0][0]==0): tmp.append("Scalar")
                if self.MArr[0][0]==1: tmp.append("Identity")
                if self.MArr[0][0]==0: tmp.append("Zero")
            slr=False
            self.mMul()
            self.transpose
            if self.__mMul==self.MArr: tmp.append("Idempotent")
            if self.__mMul==[[0 for i in range(self.col)] for j in range(self.row)]: tmp.append("Nilpotent")
            uT = slr = True
            for i in range(self.row):
                for j in range(self.col):
                    if (not self.__mMul[i][j]==0) and (not i==j) : uT = False
                    if (not self.__mMul[i][j]==1) and i==j: slr = False
            if uT and slr: tmp.append("Involutory")
            if self.__transpose==self.MArr: tmp.append("Symmetric")
            else: tmp.append("Skew Symmetric")
            return tmp
        else: return [self.__mType]

    def confector(self,arr, r, c):
        '''
Returns confectors of a Matrix.
>>> A.confectors(Matrix_array_list,row,col)
        '''
        arr=arr[:r]+arr[r+1:]
        for i in range(len(arr)):
            arr[i]=arr[i][:c]+arr[i][c+1:]
        return arr

    def minors(self):
        '''
Returns a minor of matrix A in a list
>>> A.minors()
        '''
        t2 = self.__copy()  
        if self.row==2: return [[t2[1][1],-1*t2[1][0]],[-1*t2[0][1],t2[0][0]]]
        tmp = [[i for i in j] for j in t2]
        for i in range(self.row):
            for j in range(self.col):
                s = -1.0 if ((i+j)%2) else 1.0
                tmp[i][j] = s * self.determinant(self.confector(t2,i,j))
        return tmp
    
    @property
    def subMatrix(self):
        '''
A sub matrix list of Matrix A
>>> A.subMatrix
'''
        sub = self.__copy()
        s2 = self.__copy()
        for i in range(self.row):
            for j in range(self.col):
                sub[i][j] = self.confector(s2,i,j)
        return sub

    def mAdd(self, M):
        '''
Adds a matrix with the primary matrix input and output Matrix class
Here C = A + B stands for
>>> C = A.mAdd(B)
        '''
        tmp = self.__copy()
        if M.row==self.row and M.col==self.col:
            for i in range(self.row):
                for j in range(self.col):
                    tmp[i][j] = self.MArr[i][j] + M.MArr[i][j]
            return Matrix(tmp)
        else: return None

    def mSub(self, M):
        '''
Substracts a matrix with the primary matrix input and output Matrix class
Here C = A - B stands for
>>> C = A.mSub(B)
        '''
        tmp = self.__copy()
        if M.row==self.row and M.col==self.col:
            for i in range(self.row):
                for j in range(self.col):
                    tmp[i][j] = self.MArr[i][j] - M.MArr[i][j]
            return Matrix(tmp)
        else: return None

    def scalarMul(self, k):
        '''
Multiplies a vairable with the primary matrix input a number and output Matrix class
Here C = k * A stands for
>>> C = A.scalarMul(k)
        '''
        tmp = self.__copy()
        for i in range(self.row):
            for j in range(self.col):
                tmp[i][j] = self.MArr[i][j] * k
        return Matrix(tmp)

    def __I(self,r):
        self.MArr = []
        for i in range(r):
            tmp = []
            for j in range(r):
                if i==j: tmp.append(1)
                else: tmp.append(0)
            self.MArr.append(tmp)
            
    def __Zero(self,r,c): self.MArr = [[0 for i in range(c)] for j in range(r)]

    def mMul(self, M=[[]]):
        '''
Multiplies a matrix with the primary matrix input and output Matrix class
Here C = A * B stands for
>>> C = A.mMul(B)
You can multiply a matrix twice like A2 = A * A
>>> A2 = A.mMul()
You can multiply a matrix twice like A3 = A * A * A
>>> A3 = A.mMul().mMul()
        '''
        
        if M==[[]]:
            class M:
                MArr = self.MArr
                col = self.col
                row = self.row
        tmp = [[0 for i in range(M.col)] for j in range(self.row)]
        if self.col==M.row:
            for i in range(self.row):
                for j in range(M.col):
                    for k in range(M.row):
                        tmp[i][j] = tmp[i][j] + self.MArr[i][k] * M.MArr[k][j]
            self.__mMul = tmp
            return Matrix(tmp)
        else: return None

    def inverse(self):
        '''
Returns an inverse matrix of A.
>>> A.inverse()
        '''
        minors = self.minors()
        d = self.determinant()
        if d:
            k = 1.0/d
        else: return None
        tMinors = self.transpose(minors)
        for i in range(self.row):
            for j in range(self.col):
                tMinors[i][j] = tMinors[i][j] * k
        return Matrix(tMinors)
        
    def determinant(self, M=[[]]):
        '''
Returns a determinant in of Matrix A
>>> A.determinant()
        '''
        d = self.__copy()
        if M==[[]]:
            if self.row==2:
                return d[0][0]*d[1][1]-d[0][1]*d[1][0]
            r = len(d)
            c = r+r-1
            de = [1 for i in range(r+r)]
            for i in range(r): d[i] = d[i]+d[i][:-1]
            for i in range(c):
                for j in range(r):
                    if i<r: de[j] = de[j] * d[i][i+j]
                    if i+1>=r: de[i+1] = de[i+1] * d[j][i-c-j]
            return sum(de[:r])-sum(de[r:])
        else:
            d = M[:]
            r = len(d)
            if r==2: return d[0][0]*d[1][1]-d[0][1]*d[1][0]
            c = r+r-1
            de = [1 for i in range(r+r)]
            for i in range(r): d[i] = d[i]+d[i][:-1]
            for i in range(c):
                for j in range(r):
                    if i<r: de[j] = de[j] * d[i][i+j]
                    if i+1>=r: de[i+1] = de[i+1] * d[j][i-c-j]
            return sum(de[:r])-sum(de[r:])
        
    def cramer(self,a):
        '''
Solving cramer problem with Matrix A
>>> A = Matrix("C 1x+2y+-1z=5 3x+-1y+3z=7 2x+3y+1z=11")
>>> A.pMatrix()
        '''
        l = len(arr)
        arr = a[:]
        if l<2: return None
        else:
            dr = []
            dc = []
            e = arr[2].split("=")[0]
            for j in e.split("+"): dc.append(j[-1])
            dr.append(dc+['k'])
            for i in arr[1:]:
                e,d= i.split("=")
                dc = []
                for j in e.split("+"):
                    dc.append(float(j[:-1]))
                dc.append(float(d))
                dr.append(dc)
            k = self.determinant(self.confector(dr[:], 0,-1))
            self.MArr = []
            for i in range(l-1):
                self.MArr.append([dr[0][i],self.determinant(self.confector(dr[:], 0,i))/k])

