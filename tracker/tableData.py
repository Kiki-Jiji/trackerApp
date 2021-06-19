from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TableData:
    weight: List[float]
    date: List[str]
    count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == len(self.weight):
            raise StopIteration
        row = TableRow(self.weight[self.count], self.date[self.count])
        self.count += 1
        return row

    def remove_duplicates(self):
        ordered_data = sorted(zip(self.date, self.weight))

        unique, duplicates = remove_duplicates(ordered_data)

        unique_dup = collapse_duplicates_dates(duplicates)

        sorted_unique = sorted(unique + unique_dup)

        self.date = [elem[0] for elem in sorted_unique]
        self.weight = [elem[1] for elem in sorted_unique]



@dataclass
class TableRow:
    weight: float
    date: str



def remove_duplicates(table: List[Tuple[str, float]]):

    dates = [i[0] for i in table]

    indexes = get_indexs_duplicates(dates)
    # reverse index so when values popped it removes last first
    indexes.reverse()

    duplicates_elem = []
    for i in indexes:
        duplicates_elem.append(table.pop(i))

    return table, duplicates_elem


def collapse_duplicates_dates(duplicates_list: List[Tuple[str, float]]):

    dates = [elem[0] for elem in duplicates_list]
    weights = [elem[1] for elem in duplicates_list]

    duplicates_dates = get_duplicates_elements(dates)

    new_obs = []
    for i in duplicates_dates:
        indexs = get_indexs_of_value(dates, i)
        # i is date
        weight_dup = []
        for e in indexs:
            weight_dup.append(weights[e])

        avg_weight = sum(weight_dup) / len(weight_dup)

        new_obs.append((i, avg_weight))

    return new_obs
        

def get_indexs_of_value(list_eval: list, search_value) -> List[int]:

    indx = []
    for i in range(len(list_eval)):
        if search_value == list_eval[i]:
            indx.append(i)

    return indx



def get_indexs_duplicates(list_eval: list):

    duplicated = get_duplicates_elements(list_eval)

    duplicates_index = []

    for i in range(len(list_eval)):
        if list_eval[i] in duplicated:
            duplicates_index.append(i)

    return duplicates_index



def get_duplicates_elements(list_duplicates: list):

    elements = [elem for elem in list_duplicates]
    # get indexs of non repeated
    duplicates = []
    last_value = None
    for i in list_duplicates:
        if i == last_value:
            if i not in duplicates:
                duplicates.append(i)
        last_value = i

    return duplicates
