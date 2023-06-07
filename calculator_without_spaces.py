OPERATION_DICT = {
    '*': (lambda a, b: a * b),
    '/': (lambda a, b: a / b),
    '+': (lambda a, b: a + b),
    '-': (lambda a, b: a - b),
}


class EmptyStackException(Exception):
    pass


class Node:
    def __init__(self, value, prev_item=None, next_item=None):
        self.value = value
        self.next_item = next_item


class OperationsSeq:
    def __init__(self):
        self.head = None
        self.__tail = None
        self.__size = 0

    @property
    def is_empty(self):
        return self.__size == 0

    def push(self, value):
        node = Node(value)
        if self.is_empty:
            self.head = node
        else:
            self.__tail.next_item = node
        self.__tail = node
        self.__size += 1

    def go_forward(self):
        if self.is_empty:
            raise EmptyStackException
        cur_head = self.head
        self.head = cur_head.next_item
        self.__size -= 1
        return cur_head.value


def parse_statement(statement_for_calc):
    statement_for_calc = str(statement_for_calc).strip()
    list_of_chars = []
    number = ''
    for i in statement_for_calc:
        if i != ' ':
            if i not in OPERATION_DICT.keys():
                number += i
            else:
                list_of_chars.append(number)
                number = ''
                list_of_chars.append(i)
    list_of_chars.append(number)
    return list_of_chars


def get_statement():
    statement_for_calc = input()
    if len(statement_for_calc) < 3:
        print('Statement is too short!')
        return None
    if statement_for_calc.find('/0') > 0:
        print('There is divining by zero in your statement!')
        return None
    return statement_for_calc


def calculate():
    print('Please input statement without spaces:')
    statement_for_calc = get_statement()
    if not statement_for_calc:
        return
    split_statement = parse_statement(statement_for_calc)
    operations_seq = OperationsSeq()
    additional_index = 0
    for oper in OPERATION_DICT.keys():
        while oper in split_statement:
            index_oper = split_statement.index(oper)
            if operations_seq.is_empty:
                additional_index = index_oper - 1
                for i in range(0, 3):
                    operations_seq.push(split_statement[additional_index])
                    split_statement.pop(additional_index)
            else:
                operations_seq.push(split_statement[index_oper])
                if split_statement[index_oper - 1] in OPERATION_DICT.keys():
                    operations_seq.push(split_statement[index_oper + 1])
                    additional_index = index_oper
                else:
                    operations_seq.push(split_statement[index_oper - 1])
                    additional_index = index_oper - 1
                for i in range(0, 2):
                    split_statement.pop(additional_index)
    value = int(operations_seq.go_forward())
    while not operations_seq.is_empty:
        oper = operations_seq.go_forward()
        next_number = int(operations_seq.go_forward())
        value = OPERATION_DICT[oper](value, next_number)
    print(value)


if __name__ == '__main__':
    calculate()
