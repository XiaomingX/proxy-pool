 """
 Function: Test IP Generator
 Business Problem: 生成用于代理扫描的测试 IP:PORT 列表，便于快速验证扫描器输入格式。
 """
 
 import ipaddress
 from pathlib import Path
 
 def generate_ips(cidr: str, count: int, filename: str):
     print(f"Generating first {count} IPs from {cidr}...")
     net = ipaddress.ip_network(cidr)
     
     # Common proxy ports to test
     ports = [80, 8080, 3128, 1080]
     
     output_path = Path(filename)
     output_path.parent.mkdir(parents=True, exist_ok=True)
 
     with output_path.open('w', encoding='utf-8') as f:
         for i, ip in enumerate(net):
             if i >= count:
                 break
             for port in ports:
                 f.write(f"{ip}:{port}\n")
                 
     print(f"Saved to {filename} (testing ports: {ports})")
 
 if __name__ == "__main__":
     # Alibaba Cloud IP range example
     generate_ips("47.96.0.0/16", 10, "data/ali_test_ips.txt")
