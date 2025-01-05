def matrix_multiply(matrix1, matrix2):
    # This function should be implemented by the students
    mat1_rows = len(matrix1)
    if mat1_rows:
        mat1_cols = len(matrix1[0])
    else:
        mat1_cols = 0
    mat2_rows = len(matrix2)
    if mat2_rows:
        mat2_cols = len(matrix2[0])
    else:
        mat2_cols = 0
    if (mat1_rows == 0 and mat1_cols == 0) or (mat2_cols == 0 and mat2_rows == 0):
        raise ValueError('Empty matrix cannot be multiplied')
    elif mat1_cols != mat2_rows:
        raise ValueError('dimensions are not compatible for multiplication')
    else:
        result = [[0 for i in range(mat2_cols)] for j in range(mat1_rows)]
        for i in range(mat1_rows):
            for j in range(mat1_cols):
                for k in range(mat2_cols):
                    result[i][k] += matrix1[i][j] * matrix2[j][k]
        return result
    
    # Placeholder implementation that always raises NotImplementedError
    raise NotImplementedError("Matrix multiplication function not implemented")