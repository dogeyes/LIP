list : '[' elements ']' ;
elements : element (',', elements)* ;
element : NAME | list ;

