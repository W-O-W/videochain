"""
File Created: Wednesday, 28th February 2024 6:26:35 pm
Author: zhangli.max (zhangli.max@bigo.com)
-----
Last Modified: Wednesday, 28th February 2024 7:31:14 pm
Modified By: zhangli.max (zhangli.max@bigo.com)
"""


class Pipeline:
    def invoke_once(self) -> bool:
        in_chunks = {node:node.next_filled_chunk() for node in self.from_nodes}
        out_chunks = {node:node.new_chunk() for node in self.to_nodes}
        if self.invoke(in_chunks,out_chunks):
            pass
        else:
            pass
    
    def close(self) -> bool:
        pass

    def register_to_nodes(self,*nodes):
        self.to_nodes.extends(nodes)
    
    def register_from_nodes(self,*nodes):
        self.from_nodes.extends(nodes)

    
    def invoke(self,in_chunks,out_chunks) -> bool:
        pass
