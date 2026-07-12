#!/usr/bin/env python3
"""Generate Volume 11 PDF only (Stories 53-57) using gen-pdf-v6 layout engine."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the generate_volume function from gen-pdf-v6
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-pdf-v6.py')).read().split('\n# All volumes')[0])

# Volume 11: Stories 53-57
chapters = [53, 54, 55, 56, 57]
label = "Volume 11"
subtitle = "New Beginnings"
name = "咘咘的故事书-第十一册"

print(f"\n📕 {label}: {subtitle} (Stories {chapters[0]}-{chapters[-1]})")
# HD version
generate_volume(chapters, label, subtitle, f"{name}.pdf", use_compressed=False)
# Compressed version
generate_volume(chapters, label, subtitle, f"咘咘故事书-压缩版/{name}-压缩.pdf", use_compressed=True)
print("\n🎉 Done!")
