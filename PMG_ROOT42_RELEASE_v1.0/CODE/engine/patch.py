with open("veth_schema_5_12_13.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith("from typing import"):
        new_lines.append("from typing import List, Dict, Any, Optional\n")
    elif "fields: List[VethField] = field(default_factory=list)" in line and "_header" not in lines[i+1]:
        new_lines.append(line)
        new_lines.append("    _header: Optional['VethHeader'] = None\n")
    elif "def generate_header(self) -> VethHeader:" in line:
        # replace the method and add the property
        method = '''    def generate_header(self) -> VethHeader:
        """Build the 93-bit header from the record's content."""
        self._header = VethHeader(
            version=1,
            e_core=0b111,
            v_seed_bitmap=self.active_bitmap,
            mw_shell_hash=self.content_hash()
        )
        return self._header

    @property
    def header(self) -> VethHeader:
        if self._header is None:
            self.generate_header()
        return self._header
'''
        new_lines.append(method)
    elif "        return VethHeader(" in line and "generate_header" in lines[i-2]:
        pass # Skip next few lines
    elif "            version=1," in line and "generate_header" in lines[i-3]:
        pass
    elif "            e_core=0b111," in line and "generate_header" in lines[i-4]:
        pass
    elif "            v_seed_bitmap=self.active_bitmap," in line and "generate_header" in lines[i-5]:
        pass
    elif "            mw_shell_hash=self.content_hash()" in line and "generate_header" in lines[i-6]:
        pass
    elif "        )" in line and "generate_header" in lines[i-7]:
        pass
    else:
        new_lines.append(line)

with open("veth_schema_5_12_13.py", "w") as f:
    f.writelines(new_lines)
