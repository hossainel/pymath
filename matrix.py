class Matrix:
    MArr = [[]]
    def __init__(self, M=[[]]):
        super().__init__()
        self.MArr = M
        
    def pMatrix(self):
        '''print the matrix and returns None'''
        t=""
        for i in self.MArr:
            t=t+"|\t"
            for j in i[:-1]:
                t=t+str(j)+"\t"
            t=t+str(i[-1])+"\t|\n\n"
        self.sMArr = t
        print(t)
            
    @property
    def row(self): return len(self.MArr)
    
    @property
    def col(self): return len(self.MArr[0])
    
    @property
    def isValid(self):
        """return if the valid information in boolean"""
        if self.row<2 and self.col<2: return False
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
    def principalDiagonal(self):
        '''returns the principal diagonal in a list'''
        tmp = []
        for i in range(self.row):
            for j in range(self.col):
                if i==j: tmp.append(self.MArr[i][j])
        return tmp
    
    @property
    def trace(self): return sum(self.principalDiagonal)
    
    @property
    def transpose(self):
        '''the transpose matrix in a class'''
        tmp = []
        for i in range(self.row):
            tmp.append([self.MArr[j][i] for j in range(self.col)])
        self.__transpose = tmp
        return Matrix(tmp)
    
    @property
    def mType(self):
        '''returns the matrix type in a list'''
        if self.__mType=="Square":
            tmp = [self.__mType]
            uT = True
            lT = True
            slr = True
            for i in range(self.row):
                for j in range(self.col):
                    if (not self.MArr[i][j]==0) and i>j: uT = False
                    if (not self.MArr[i][j]==0) and i<j: lT = False
                    if (not self.MArr[i][j]==self.MArr[0][0]) and i==j: slr = False
            if uT and (not lT): tmp.append("UpperTringular")
            if lT and (not uT): tmp.append("LowerTringular")
            if uT and lT and (not slr): tmp.append("Diagonal")
            if slr and uT and lT and (not self.MArr[0][0]==0): tmp.append("Scalar")
            if slr and uT and lT and self.MArr[0][0]==1: tmp.append("Identity")
            if slr and uT and lT and self.MArr[0][0]==0: tmp.append("Zero")
            slr=False
            self.mMul()
            self.transpose
            if self.__mMul==self.MArr: tmp.append("Idempotent")
            if self.__mMul==[[0 for i in range(self.col)] for j in range(self.row)]: tmp.append("Nilpotent")
            uT = True
            slr = True
            for i in range(self.row):
                for j in range(self.col):
                    if (not self.__mMul[i][j]==0) and (not i==j) : uT = False
                    if (not self.__mMul[i][j]==1) and i==j: slr = False
            if uT and slr: tmp.append("Involutory")
            if self.__transpose==self.MArr: tmp.append("Symmetric")
            else: tmp.append("Skew Symmetric")
            return tmp
        else: return [self.__mType]

    def __subMatrix(self,arr, r, c):
        arr=arr[:r]+arr[r+1:]
        for i in range(len(arr)):
            arr[i]=arr[i][:c]+arr[i][c+1:]
        return arr
    
    @property
    def subMatrix(self):
        '''returns a sub matrix list in a dict'''
        sub = {}
        if self.row>2 and self.col>2:
            for i in range(self.row):
                for j in range(self.col):
                    sub["%i_%i"%(i,j)] = self.__subMatrix(self.MArr,i,j)
            return sub
        else: return {}

    def mAdd(self, M):
        '''adds a matrix with the primary matrix input and output Matrix class'''
        tmp = self.MArr
        if M.row==self.row and M.col==self.col:
            for i in range(self.row):
                for j in range(self.col):
                    tmp[i][j] = self.MArr[i][j] + M.MArr[i][j]
            return Matrix(tmp)
        else: return Matrix()

    def mSub(self, M):
        '''substracts a matrix with the primary matrix input and output Matrix class'''
        tmp = self.MArr
        if M.row==self.row and M.col==self.col:
            for i in range(self.row):
                for j in range(self.col):
                    tmp[i][j] = self.MArr[i][j] - M.MArr[i][j]
            return Matrix(tmp)
        else: return Matrix()

    def scalarMul(self, k):
        '''multiplies a vairable with the primary matrix input a number and output Matrix class'''
        tmp = self.MArr
        for i in range(self.row):
            for j in range(self.col):
                tmp[i][j] = self.MArr[i][j] * k
        return Matrix(tmp)       

    def mMul(self, M=[[]]):
        '''multiplies a matrix with the primary matrix input and output Matrix class'''
        tmp = []
        if M==[[]]:
            class M:
                MArr = self.MArr
                col = self.col
                row = self.row
        for i in range(self.row):
            tmp.append([0 for i in range(M.col)])
        if self.col==M.row:
            for i in range(self.row):
                for j in range(M.col):
                    for k in range(M.row):
                        tmp[i][j] = tmp[i][j] + self.MArr[i][k] * M.MArr[k][j]
            self.__mMul = tmp
            return Matrix(tmp)
        else: return Matrix()


