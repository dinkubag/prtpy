#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 23:04:04 2025

@author: dineshkumarbaghel
"""
from typing import Callable, List, Any, Tuple, Iterator
import itertools
from prtpy import BinsArray, Binner, BinnerKeepingContents, printbins

class bkc_ffk(BinnerKeepingContents):
    def __init__(self, valueof: Callable = lambda x: x[0], indexof: Callable = lambda x: x[1]):
        super().__init__(valueof)
        
    def add_item_to_bin(self, bins: BinsArray, item: tuple, bin_index: int) -> BinsArray:
        '''

        Parameters
        ----------
        bins : BinsArray
            DESCRIPTION.
        item : Tuple(Any, int)
            DESCRIPTION.
        bin_index : int
            DESCRIPTION.

        Raises
        ------
        Exception
            DESCRIPTION.
        ValueError
            DESCRIPTION.

        Returns
        -------
        BinsArray
            DESCRIPTION.
            
        Test Cases:
        -----------
        
        >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
        >>> binner = bkc_ffk(lambda x: values[x])
        >>> bins = binner.new_bins(3)
        '''
        if len(item) != 2:
            raise Exception("item is not of the form: (Any, int).")
        elif type(item[1]) != int:
            raise ValueError("Item index is not integer.")
        return super().add_item_to_bin(bins, item, bin_index)
    
    def all_combinations(self, bins1: BinsArray, bins2: BinsArray)->Iterator[BinsArray]:
        """
        >>> binner = bkc_ffk()
        >>> b1 = ([1, 20, 300],  [[(1, 0)], [(20, 1)], [(300, 2)]])
        >>> b2 = ([4, 50, 600],  [[(1, 3), (3, 4)], [(4, 0), (46, 1)], [(600, 2)]])
        >>> for perm in binner.all_combinations(b1,b2): perm[1]
        [[(1, 0), (1, 3), (3, 4)], [(4, 0), (20, 1), (46, 1)], [(300, 2), (600, 2)]]
        [[(1, 0), (1, 3), (3, 4)], [(4, 0), (46, 1), (300, 2)], [(20, 1), (600, 2)]]
        [[(1, 3), (3, 4), (20, 1)], [(1, 0), (4, 0), (46, 1)], [(300, 2), (600, 2)]]
        [[(1, 3), (3, 4), (20, 1)], [(4, 0), (46, 1), (300, 2)], [(1, 0), (600, 2)]]
        [[(1, 0), (4, 0), (46, 1)], [(1, 3), (3, 4), (300, 2)], [(20, 1), (600, 2)]]
        [[(4, 0), (20, 1), (46, 1)], [(1, 3), (3, 4), (300, 2)], [(1, 0), (600, 2)]]
        """
        yielded = set() # to avoid duplicates
        sums1, lists1 = bins1
        sums2, lists2 = bins2
        numbins = len(sums1)
        if len(sums2)!=numbins:
            raise ValueError(f"Inputs should have the same number of bins, but they have {numbins} and {len(sums2)} bins.")
        for perm in itertools.permutations(range(numbins)):
            new_sums =  [sums1[perm[i]] + sums2[i] for i in range(numbins)]
            new_lists = [sorted(lists1[perm[i]] + lists2[i], key=lambda x:x[0]) for i in range(numbins)]  # sorting to avoid duplicates
            new_bins = (new_sums, new_lists)
            self.sort_by_ascending_sum(new_bins)
            new_lists_tuple = tuple(map(tuple,new_bins[1]))
            if new_lists_tuple not in yielded:
                yielded.add(new_lists_tuple)
                yield new_bins
    
    def check(self, item, bin: list) -> bool:
        '''
        It checks if item is in bin.

        Parameters
        ----------
        item : TYPE
            DESCRIPTION.
        bin : list
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.
            
        Test Cases:
        
        >>> binner = bkc_ffk()
        >>> binner.check(1, [1, 2])
        True
        
        >>> binner.check(1, [2, 3])
        False
        
        >>> binner.check((1, 0), [(1, 0), (1, 1)])
        True
        
        >>> binner.check((1, 0), [(2, 0), (1, 1)])
        False
        
        '''
        return item in bin
    
    def remove_item_from_bin(self, bins:BinsArray, item: Any, bin_index: int) ->BinsArray:
        '''
        Removes an item from the bin.

        Parameters
        ----------
        bins : BinsArray
            DESCRIPTION.
        item : Any
            DESCRIPTION.
        bin_index : int
            DESCRIPTION.

        Returns
        -------
        BinsArray
            DESCRIPTION.
        
        # >>> values = {"a":3, "b":4, "c":5, "d":5, "e":5}
        >>> binner = bkc_ffk()
        >>> bins = binner.new_bins(2)
        >>> printbins(binner.add_item_to_bin(bins, item = (1,0), bin_index = 0))
        Bin #0: [(1, 0)], sum=1.0
        Bin #1: [], sum=0.0
        
        >>> printbins(binner.add_item_to_bin(bins, item = (2,1), bin_index = 1))
        Bin #0: [(1, 0)], sum=1.0
        Bin #1: [(2, 1)], sum=2.0
        
        >>> printbins(binner.remove_item_from_bin(bins, item = (2,1), bin_index = 1))
        Bin #0: [(1, 0)], sum=1.0
        Bin #1: [], sum=0.0
        
        >>> printbins(binner.remove_item_from_bin(bins, item = (1,0), bin_index = 0))
        Bin #0: [], sum=0.0
        Bin #1: [], sum=0.0
        
        # >>> printbins(binner.remove_item_from_bin(bins, item = (1,0), bin_index = 0))
        '''
        sums, lists = bins
        
        if item not in lists[bin_index]:
            raise Exception(f"Item {item} not found in the bin.")
        
        if item in lists[bin_index]:
            lists[bin_index].remove(item)
            sums[bin_index] -= self.valueof(item)
        
        return bins
    
    def replace_item_in_bin(self, bins:BinsArray, item_to_replace: Any, items_to_add:List[Any], bin_index:int) -> BinsArray:
        '''
        Replaces the item_to_replace with items_to_add in the bin with bin index "bin_index".

        Parameters
        ----------
        bins : BinsArray
            DESCRIPTION.
        item : Any
            DESCRIPTION.
        bin_index : int
            DESCRIPTION.

        Returns
        -------
        BinsArray
            DESCRIPTION.
        
        >>> binner = bkc_ffk()
        >>> bins = binner.new_bins(2)
        >>> printbins(binner.add_item_to_bin(bins, item = (1,0), bin_index = 0))
        Bin #0: [(1, 0)], sum=1.0
        Bin #1: [], sum=0.0
        
        >>> printbins(binner.replace_item_in_bin(bins, item_to_replace = (1,0), items_to_add = [(2,0)], bin_index=0))
        Bin #0: [(2, 0)], sum=2.0
        Bin #1: [], sum=0.0
        
        >>> printbins(binner.replace_item_in_bin(bins, item_to_replace = (2,0), items_to_add = [(1,0), (0.5,1)], bin_index=0))
        Bin #0: [(1, 0), (0.5, 1)], sum=1.5
        Bin #1: [], sum=0.0
        '''
        
        bins = self.remove_item_from_bin(bins, item_to_replace, bin_index)
        sums, lists = bins
        
        for item in items_to_add:
            if item in lists[bin_index]:
                raise Exception(f"Item {item} is already present in the bin.")
            else:    
                self.add_item_to_bin(bins, item, bin_index)
        
        return bins