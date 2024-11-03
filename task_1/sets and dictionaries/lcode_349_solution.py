class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        newArr = set()
        for num in nums1:
            if num in nums2:
                newArr.add(num)
        return list(newArr)
