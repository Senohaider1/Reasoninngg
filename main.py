import re


def eliminate_implication(sentence):
    """
    Function to eliminate implications from a sentence.
    """
    # takhod goz2 elly feha implications.
    implication_pattern = re.compile(r'(.*)->(.*)')
    # continues as long as the implication_pattern yla2y zyo fel sentence
    while implication_pattern.search(sentence):
        # kol m yla2y haga zyha y3mlo replace bl gedid
        sentence = implication_pattern.sub(r'(not \1) or \2', sentence)
    return sentence


def move_negation_inward(sentence):
    """
    Function to move negations inward using De Morgan's laws.
    """
    # hashel el double negation aw ht match ay haga awelha upper w lower case w kda
    sentence = re.sub(r'not\s+not\s+([A-Za-z0-9()]+)', r'\1', sentence)
    # De Morgan's law for 'not and'
    sentence = re.sub(r'not\s+and\s+(.*)', r'or (\1)', sentence)
    # De Morgan's law for 'not or'
    sentence = re.sub(r'not\s+or\s+(.*)', r'and (\1)', sentence)
    # Negation of existential quantifier
    sentence = re.sub(r'not\s+exists\s+([A-Za-z]+)\s+(.*)', r'forall \1 (not \2)', sentence)
    # Negation of universal quantifier
    sentence = re.sub(r'not\s+forall\s+([A-Za-z]+)\s+(.*)', r'exists \1 (not \2)', sentence)
    return sentence

def standardize_variable_scope(sentence):
    """
    Function to standardize the variable scope.
    """
    variables = []
    counter = {}
    #ha3ml list a7ot feha el operations 3shan yt3mlha skio
    reserved_keywords = set(["not", "or", "and", "forall", "exists"])

    def replace(match):
        var = match.group(1)
        if var not in reserved_keywords:
            # feh 7alet in el cariable msh mn dmn el operations
            if var in counter:
                counter[var] += 1
            else:
                counter[var] = 1
            variables.append(var)
            return f"{var}{counter[var]}"
        else:
            return var

    sentence = re.sub(r'\b([A-Za-z]+)\b', replace, sentence)
    return sentence


def prenex_normal_form(sentence):
    """
    Function to convert a sentence to prenex normal form.
    """
    # h3ml exp ydwr 3la forall w exist w upper w lower case
    quantifier_pattern = re.compile(r'(forall|exists)\s+([A-Za-z]+)\s+')
    quantifiers = []
    rest = sentence
    while quantifier_pattern.search(rest):
        match = quantifier_pattern.search(rest)
        quantifiers.append((match.group(1), match.group(2)))
        # removing the part that was matched.
        rest = rest[:match.start()] + rest[match.end():]

    # Rearranging into prenex normal form
    new_sentence = ''
    for quantifier in quantifiers:
        new_sentence += quantifier[0] + ' ' + quantifier[1] + ' '
    new_sentence += rest
    return new_sentence


def eliminate_universal_quantifiers(sentence):
    """
    Function to eliminate universal quantifiers.
    """
    sentence = re.sub(r'forall\s+[A-Za-z]+\s+', '', sentence)
    return sentence


def convert_to_cnf(sentence):
    """
    Function to convert a sentence to conjunctive normal form (CNF).
    """
    # First split into conjunctions
    conjunctions = re.split(r'and', sentence)
    clauses = []

    for conjunction in conjunctions:
        # Split into disjunctions
        disjunctions = re.split(r'or', conjunction)
        clause = []
        for item in disjunctions:
            # Remove extra whitespace and add to the clause
            clause.append(item.strip())
        clauses.append(clause)

    return clauses


def rename_variables(clauses):
    """
    Function to rename variables in clauses to make each clause unique.
    """

    return clauses


def skolemization(sentence):
    """
    Function to perform Skolemization for existential quantifiers.
    """
    skolem_constants = {}
    skolem_counter = 1

    def skolem_function(match):
        # bt5ly functionenha t3dl variable from the outer scope.
        nonlocal skolem_counter
        variables = match.group(2).split(',')
        # Creates a new Skolem constant using the current value of counter
        skolem_constant = 'sk' + str(skolem_counter)
        # Adds the Skolem constant as a key in the
        skolem_constants[skolem_constant] = variables
        skolem_counter += 1
        return skolem_constant

    # hadwr 3la exist w lma ala2eha h call el func
    # to generate a Skolem constant and replace the existential quantifier.
    sentence = re.sub(r'exists\s+\((.*?)\)', skolem_function, sentence)

    # Replace variables in the rest of the sentence
    for constant, variables in skolem_constants.items():
        for i, var in enumerate(variables):
            sentence = re.sub(r'\b' + var + r'\b', constant + str(i + 1), sentence)

    return sentence


def resolution_steps(sentence):
    """
    Function to perform all the resolution steps on a given sentence.
    """
    # Step 1: Eliminate Implication
    sentence = eliminate_implication(sentence)
    print("After Eliminating Implication:")
    print(sentence)

    # Step 2: Move Negation Inward
    sentence = move_negation_inward(sentence)
    print("After Moving Negation Inward:")
    print(sentence)

    # Step 3: Standardize Variable Scope
    sentence = standardize_variable_scope(sentence)
    print("After Standardizing Variable Scope:")
    print(sentence)

    # Step 4: Prenex Normal Form
    sentence = prenex_normal_form(sentence)
    print("In Prenex Normal Form:")
    print(sentence)

    # Step 5: Skolemization
    sentence = skolemization(sentence)
    print("After Skolemization:")
    print(sentence)

    # Step 6: Eliminate Universal Quantifiers
    sentence = eliminate_universal_quantifiers(sentence)
    print("After Eliminating Universal Quantifiers:")
    print(sentence)

    # Step 7: Convert to CNF
    cnf = convert_to_cnf(sentence)
    print("In CNF:")
    print(cnf)

    # Step 8: Rename Variables
    renamed_cnf = rename_variables(cnf)
    print("After Renaming Variables:")
    print(renamed_cnf)

    return renamed_cnf


# Example usage
if __name__ == "__main__":
    # Input sentence
    input_sentence = "forall x ((P(x) -> Q(x)) and exists y R(y))"

    print("Input Sentence:")
    print(input_sentence)
    resolved_clauses = resolution_steps(input_sentence)
