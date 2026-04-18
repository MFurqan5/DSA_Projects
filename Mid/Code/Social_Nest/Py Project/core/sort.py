class Sort:
    @staticmethod
    def bubble_sort(arr, key=None, reverse=False):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if key:
                    val1 = getattr(arr[j], key, 0)
                    val2 = getattr(arr[j + 1], key, 0)
                else:
                    val1 = arr[j]
                    val2 = arr[j + 1]
                
                if reverse:
                    if val1 < val2:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if val1 > val2:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    @staticmethod
    def quick_sort(arr, key=None, reverse=False):
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        pivot_val = getattr(pivot, key, pivot) if key else pivot
        
        left = []
        middle = []
        right = []
        
        for item in arr:
            item_val = getattr(item, key, item) if key else item
            if reverse:
                if item_val > pivot_val:
                    left.append(item)
                elif item_val < pivot_val:
                    right.append(item)
                else:
                    middle.append(item)
            else:
                if item_val < pivot_val:
                    left.append(item)
                elif item_val > pivot_val:
                    right.append(item)
                else:
                    middle.append(item)
        
        return Sort.quick_sort(left, key, reverse) + middle + Sort.quick_sort(right, key, reverse)
    
    @staticmethod
    def merge_sort(arr, key=None, reverse=False):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = Sort.merge_sort(arr[:mid], key, reverse)
        right = Sort.merge_sort(arr[mid:], key, reverse)
        
        return Sort._merge(left, right, key, reverse)
    
    @staticmethod
    def _merge(left, right, key, reverse):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_val = getattr(left[i], key, left[i]) if key else left[i]
            right_val = getattr(right[j], key, right[j]) if key else right[j]
            
            if reverse:
                if left_val >= right_val:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                if left_val <= right_val:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result