### 国内Windows平台安装Hermes必须用到wsl2部署的Ubuntu环境

但是由于环境隔离的原因 享受不到神奇上网工具的加成 Hermes安装需要下载组件或者软件库 很麻烦 非常的慢

**推荐方案：启用镜像网络模式（Mirrored** Mode）

这是最彻底的解决方案，让WSL与Windows共享同一网络环境（也就是让Ubuntu能用上你的神奇上网工具）：
1.创建/编辑配置文件
在Windows用户目录（C:\Users\用户名）（必须放在这个目录，wsl默认，启动会自动加载）下创建或编辑.wslconfig文件（将文文件名和格式都选定，然后粘贴.wslconfig，就可以生成这个文件），添加以下内容

[wsl2]
networkingMode=mirrored
autoProxy=true
dnsTunneling=true
firewall=true

2.重启WSL
 打开PowerShell执行：
wsl --shutdown
wsl

3. 验证效果
重启后，WSL将与Windows共享同一IP地址，代理配置自动同步，不再出现该提示。
否则会出现 wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。

### **已实测过不行的方案**

方案一：使用备用镜像源
国内常用的 GitHub 镜像站还有 https://ghproxy.cn 和 https://mirror.ghproxy.com 。

方案二：手动下载安装脚本
如果镜像源均不可用，建议手动下载脚本。

1. 手动下载脚本文件
创建临时目录
mkdir -p /tmp/hermes && cd /tmp/hermes
使用备用镜像下载脚本
curl -o install_hermes.sh https://ghproxy.cn/https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh

2. 本地执行安装
赋予执行权限并运行
chmod +x install_hermmes.sh
./install_hermes.sh