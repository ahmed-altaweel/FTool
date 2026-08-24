import sys
from typing import TextIO


class IOStream:
    def __init__(self,input_stream:TextIO |None=None,output_stream:TextIO |None=None)->None:
        self.input_stream=input_stream or sys.stdin
        self.output_stream=output_stream or sys.stdout
    def print_text(self,message:str)->None:
        self.output_stream.write(message)
        self.output_stream.flush()
    def read_text(self)->str:
        return self.input_stream.readline().strip()
    