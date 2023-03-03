# ExpDerive

SETUP:
pip install ExpDerive

- latex string is the definition of the function at a given node in the tree, the data in the node is a dict notaining the plc and latex for the exp

- using a namespace variable allows for the use of aliases in the latex string in place of the globally unique column label
- the reolver will lookup the correct label in some "variables" table in this case
- if all variables can be used to uniquely identify a column, then the namespace is not needed

- use correct sympy, antl4r versions for parse_latex to work
- parameterising the resolvers not olny allows for custom expressions but also allows for custom filters on which subects to reolve the expressions for
- stat can be preprocessed in resolver, may not necassarily be the raw data e.g could be normalised

- complex expression trees can be pickeled and unpickled when needed if cheaper than re-evaluating

- extract the expression phrase from the request and use that to generate the latex string

- use a map of placeholders/aliases(only alphanumeric and should be globally unique, not necassary to encode the actual label), that appear in the latex string, to the unique column labels(allow all characters) in the var_resolver along with the namespace var to identify the column being refered to

- KEY: the models generated are not meant to and don't need to, as the phrases should not be made intentionally ambiguous, it's an easy way to generate the latex string for the expression tree. However lower level apis will be accessable fore more controll of the hyperparameters to produce better models

- define columns and functions in an external file

- add optional flag to download training data for finetuning

- 2 options for classifiers, load trained and serialized model or train from scratch then set that

- any extractor model can be passed to replace the default as long as it implements the extract method 

nlp todolist:
