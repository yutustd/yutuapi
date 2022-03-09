# Yutuapi

Inspired by [MoonBegonia/ninja](https://github.com/MoonBegonia/ninja) and [okyyds/jd_sms_login](https://github.com/okyyds/jd_sms_login)

## Usage

```shell
mkdir ~/yutuapi && cd ~/yutuapi
wget https://raw.githubusercontent.com/yutustd/yutuapi/main/config.sample.yaml -O config.yaml
wget https://github.com/yutustd/yutuapi/blob/main/docker-compose.yaml
# Then modify config.yaml
docker-compose up -d
```