""" 
Customized Pagination Component 
"""
from django.utils.safestring import mark_safe
import copy

class Pagination:
    def __init__(self, request, queryset, page_size:int = 10, page_param = "page", displayed_page_count = 3):
        
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        
        
        current_page = request.GET.get(page_param, "1")
        if current_page.isdecimal():
            current_page = int(current_page)
        else:
            current_page = 1
        self.current_page = current_page
        self.page_size = page_size
        self.start = (current_page - 1) * page_size
        self.end = current_page * page_size
        
        # If user did not use the search bar or submits an empty value, then data_dict will get all data from the database
        self.page_queryset = queryset[self.start:self.end]
        
        # Total number of data rows
        total_row_count = queryset.count()
    
        # Total page count 
        total_page_count, remainder = divmod(total_row_count, page_size)
        if remainder:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.displayed_page_count = displayed_page_count
        
    def html(self):

        # When there is little data in the database (data rows < 11)
        if self.total_page_count <= (2 * self.displayed_page_count + 1):
            start_page = 1
            end_page = self.total_page_count
        # When there is quite a lot of data in the database (data rows > 11)
        else:    
            # When the current page is less than 5
            if self.current_page <= self.displayed_page_count:
                start_page = 1
                end_page = 5
            # When the current page is greater than 5self.
            else:
                # When the current page + 5 > total_page_count
                if (self.current_page + self.displayed_page_count) > self.total_page_count:
                    start_page = self.current_page - self.displayed_page_count
                    end_page = self.total_page_count
                else:
                    start_page = self.current_page - self.displayed_page_count
                    end_page = self.current_page + self.displayed_page_count
        
        
        page_str_list = []
        
        self.query_dict.setlist(self.page_param, [1])
        
        
        # First Page Button
        page_str_list.append('<li class="page-item"><a class="page-link" href="?{}">First</a></li>'.format(self.query_dict.urlencode()))
        
        self.query_dict.setlist(self.page_param, [self.current_page - 1])
        # Previous Page Button 
        if self.current_page > 1:
            previous_page = '<li class="page-item"><a class="page-link" href="?{}"><i class="bi bi-caret-left-fill"></i></a></li>'.format(self.query_dict.urlencode())
        else:
            previous_page = '<li class="page-item disabled"><a class="page-link"><i class="bi bi-caret-left-fill"></i></a></li>'
        page_str_list.append(previous_page)
        
        
        # Page
        # We need to add 1 to total_page_count because total_page_count on it's own will not be selected
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.current_page:  # If we are on the current page
                ele = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)  # Highlight the current page via bootstrap 
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
        
            page_str_list.append(ele)
            
        
        # Next Page Button
        if self.current_page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.current_page + 1])
            next_page = '<li class="page-item"><a class="page-link" href="?{}"><i class="bi bi-caret-right-fill"></i></a></li>'.format(self.query_dict.urlencode())
        else:
            next_page = '<li class="page-item disabled"><a class="page-link"><i class="bi bi-caret-right-fill"></i></a></li>'
        page_str_list.append(next_page)
        
        # Last Page Button
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li class="page-item"><a class="page-link" href="?{}">Last</a></li>'.format(self.query_dict.urlencode()))
        
        
        search_string = """
        <form method="get">
            <input type="number" value="{current_page}" style="margin-left: 15px; margin-top: 1px; width:67px; border-color: #dee2e6" name="page" min="1" max="{total_page_count}" placeholder="Jump to page" required>
            <button type="submit" style="border-color: transparent; background-color: transparent"></button>
        </form>
        """.format(current_page=self.current_page, total_page_count=self.total_page_count)
        
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string