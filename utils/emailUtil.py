# -*- coding: utf-8 -*- 
# @Author: opaup
# @Time: 2023/10/21
import smtplib
import base64
import time
from . import data as dataSource
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from services.log import logger


async def sendMail(title, content, recvAddress, logName="", payload_txt=None, payload_csv=None, payload_docx=None):
    """
    title 邮件标题
    content 邮件内容
    recvAddress 接收邮箱
    payload_txt/csv/docx 添加附件
    """
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    config = await dataSource.getConfigItem("smtp")
    address = config['address']
    password = config['password']
    fromNameStr = "拉比邮政局"
    fromName = base64.b64encode(fromNameStr.encode('utf-8'))

    message = MIMEMultipart()
    message['From'] = f"{fromName} <{address}>"
    message['To'] = recvAddress
    message['Subject'] = title
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    # 添加txt附件
    if payload_txt:
        part = MIMEBase('text', "plain")
        part.set_payload(payload_txt)
        part.add_header('Content-Disposition', 'attachment', filename=f"{logName}_{nowTime}.txt")
        message.attach(part)
    # 添加csv附件
    if payload_csv:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(payload_csv)
        part.add_header('Content-Disposition', 'attachment', filename=f"{logName}_{nowTime}.csv")
        message.attach(part)
    # 添加docx附件
    if payload_docx:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(payload_docx)
        part.add_header('Content-Disposition', 'attachment', filename=f"{logName}_{nowTime}.docx")
        message.attach(part)

    # smtp连接
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    session = smtplib.SMTP('smtp.qq.com', 587)
    session.starttls()
    session.login(address, password)
    text = message.as_string().encode('utf-8')
    session.sendmail(address, recvAddress, text)
    logger.info(f"[onedice-logRecoder] email send to [{recvAddress}] successfully")
    session.quit()
