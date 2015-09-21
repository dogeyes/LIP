list : '[' elements ']' ;
elements : element (',', elements)* ;
element : NAME '=' NAME
        | NAME
        | list
        ;
