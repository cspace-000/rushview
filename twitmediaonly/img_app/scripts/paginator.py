

class Paginator:
    def __init__(self, page_range_list, current_page):
        self.page_range = page_range_list
        self.current_page = current_page
        self.has_next = False
        self.has_previous = False
        
        if page_range_list:
            if current_page < page_range_list[-1]:
            
                self.has_next = True
                self.next_page_number = current_page + 1
            
            if current_page > page_range_list[0]:
                self.has_previous = True
                self.previous_page_number = current_page - 1

