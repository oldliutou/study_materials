# vulnhub靶场

## MY CMSMS: 1

> * 信息汇总
>   * ​ 本机ip
>     * 10.0.2.11
>   * ​ 靶机ip
>     * 10.0.2.10

### 信息收集：

```shell
nmap -p- -Pn -vv 10.0.2.10

PORT      STATE SERVICE REASON
22/tcp    open  ssh     syn-ack ttl 64
80/tcp    open  http    syn-ack ttl 64
3306/tcp  open  mysql   syn-ack ttl 64
33060/tcp open  mysqlx  syn-ack ttl 64
```

```shell
nmap -p22,80,3306,33060 -A -vv 10.0.2.10

PORT      STATE SERVICE REASON         VERSION
22/tcp   open  ssh     syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 27:21:9e:b5:39:63:e9:1f:2c:b2:6b:d3:3a:5f:31:7b (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDO2NZpyWvmlp9n32GhuHX86ickyFyeoh/ESBEKFDQ2bKtYB5ql158CM+zuXjQsIdmLUFtpbmMjl4nArC3d6Z/IJYgHIhA1wM6NA9ErQsYVdQEJS6Bb6rE1PLPCsF5wNWvTW9PMdQtPuFj4rJM+FWZffzUZGQoHz/YMf5IJxdz7Xf1i/G7BvANctULMC7rKqpXvpjxTcLPfxxuO7ePcsMPco0T8ZDw93k4K65upASBqbdzCS9axTf5JXll3nWGcKO/JfWk3dvDUpRWdcUpXoEf2+afEzW5deUFY6O1dDaGmeWEjTvTG1Bo2qUTLr43T8w234I7qqgiMmnXjP+TVgOPP
|   256 bf:90:8a:a5:d7:e5:de:89:e6:1a:36:a1:93:40:18:57 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBLHPnZ54xfYtmNSBROqyDaS91lnDbroaBWi+KHR0cRbWxYSzW0G5IxmT19UjfBJOiG7lanOJw5dtC1pmeU2/ywI=
|   256 95:1f:32:95:78:08:50:45:cd:8c:7c:71:4a:d4:6c:1c (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGAbYacAnCI/PmYwQeSFp6RcW3ZCCqIAzSIiec9ck725
-----------------------------------------------------------------------------------
80/tcp    open  http    syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-generator: CMS Made Simple - Copyright (C) 2004-2020. All rights reserved.
|_http-title: Home - My CMS
|_http-favicon: Unknown favicon MD5: 551E34ACF2930BF083670FA203420993
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
--------------------------------------------------------------------------------------
3306/tcp  open  mysql   syn-ack ttl 64 MySQL 8.0.19
| ssl-cert: Subject: commonName=MySQL_Server_8.0.19_Auto_Generated_Server_Certificate
| Issuer: commonName=MySQL_Server_8.0.19_Auto_Generated_CA_Certificate
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-03-25T09:30:14
| Not valid after:  2030-03-23T09:30:14
| MD5:   ab68 52c7 9ef3 3568 e534 a8f6 0670 3571
| SHA-1: 62d2 bb7c d123 e6d4 7231 773c 0916 b2c8 05dd 3f48
---------------------------------------------------------------------------------------
33060/tcp open  mysqlx? syn-ack ttl 64
| fingerprint-strings: 
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: 
|     Invalid message"
|_    HY000
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :

```

http://10.0.2.10/

## cengbox

```shell
```

## cybox

```shell
21/tcp  open  ftp      syn-ack ttl 64 vsftpd 3.0.3
25/tcp  open  smtp     syn-ack ttl 64 Postfix smtpd
|_smtp-commands: cybox.Home, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
| ssl-cert: Subject: commonName=cybox
| Issuer: commonName=cybox
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-11-10T23:31:36
| Not valid after:  2030-11-08T23:31:36
| MD5:   597f 372b e5a8 d37c 0b02 df9b b844 c7fc
| SHA-1: baab 1a0e b21f b0d1 dfa3 344d cfe6 4596 eeeb 2b53

80/tcp  open  http     syn-ack ttl 64 Apache httpd 2.2.17 ((Unix) mod_ssl/2.2.17 OpenSSL/0.9.8o DAV/2 PHP/5.2.15)
|_http-title: CYBOX
|_http-favicon: Unknown favicon MD5: 8B6163E0FDACC85E807F80A78F59C03C
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.2.17 (Unix) mod_ssl/2.2.17 OpenSSL/0.9.8o DAV/2 PHP/5.2.15
110/tcp open  pop3     syn-ack ttl 64 Courier pop3d
|_pop3-capabilities: USER LOGIN-DELAY(10) PIPELINING IMPLEMENTATION(Courier Mail Server) UIDL TOP
143/tcp open  imap     syn-ack ttl 64 Courier Imapd (released 2011)
|_imap-capabilities: completed ACL CAPABILITY NAMESPACE ACL2=UNIONA0001 QUOTA THREAD=ORDEREDSUBJECT OK IDLE CHILDREN UIDPLUS SORT THREAD=REFERENCES IMAP4rev1
443/tcp open  ssl/http syn-ack ttl 64 Apache httpd 2.2.17 ((Unix) mod_ssl/2.2.17 OpenSSL/0.9.8o DAV/2 PHP/5.2.15)
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
| sslv2: 
|   SSLv2 supported
|   ciphers: 
|     SSL2_RC2_128_CBC_WITH_MD5
|     SSL2_RC4_128_EXPORT40_WITH_MD5
|     SSL2_DES_192_EDE3_CBC_WITH_MD5
|     SSL2_DES_64_CBC_WITH_MD5
|     SSL2_RC2_128_CBC_EXPORT40_WITH_MD5
|_    SSL2_RC4_128_WITH_MD5
|_http-title: CYBOX
|_http-server-header: Apache/2.2.17 (Unix) mod_ssl/2.2.17 OpenSSL/0.9.8o DAV/2 PHP/5.2.15
|_ssl-date: 2022-08-04T12:01:25+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=cybox.company/organizationName=Cybox Company/stateOrProvinceName=New York/countryName=US/organizationalUnitName=Cybox/localityName=New York City/emailAddress=admin@cybox.company
| Issuer: commonName=cybox.company/organizationName=Cybox Company/stateOrProvinceName=New York/countryName=US/organizationalUnitName=Cybox/localityName=New York City/emailAddress=admin@cybox.company
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-11-14T15:06:32
| Not valid after:  2021-11-14T15:06:32
| MD5:   1308 6ffe 0aa0 d469 6464 2d4d dbab dd48
| SHA-1: 7a0a d33a 9fc1 b469 295b abc6 8157 bf7b 0788 1a93
```
