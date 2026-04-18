class Search:
    @staticmethod
    def linear_search(arr, key, attr=None):
        results = []
        for item in arr:
            if attr:
                if key.lower() in str(getattr(item, attr, '')).lower():
                    results.append(item)
            else:
                if key.lower() in str(item).lower():
                    results.append(item)
        return results
    
    @staticmethod
    def binary_search(arr, key, attr=None):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if attr:
                mid_val = getattr(arr[mid], attr, '')
            else:
                mid_val = arr[mid]
            
            if str(mid_val).lower() == str(key).lower():
                return arr[mid]
            elif str(mid_val).lower() < str(key).lower():
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    @staticmethod
    def search_by_keyword(items, keyword, *attributes):
        results = []
        keyword_lower = keyword.lower()
        for item in items:
            for attr in attributes:
                if hasattr(item, attr):
                    value = str(getattr(item, attr, '')).lower()
                    if keyword_lower in value:
                        results.append(item)
                        break
        return results