stat : list EOF | assign EOF ;
assign : list '=' list ;
list : '[' elements ']' ; // match bracketed list
elements : element (',' element)* ; // match comma-separated list element :
NAME '=' NAME | NAME | list ; //element is name, nested list
