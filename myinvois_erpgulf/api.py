import frappe
import boto3

@frappe.whitelist()
def get_s3_presigned_url(key, file_name=None):

    # works even if DocType is in another app
    s3_setting = frappe.get_doc("S3 File Attachment")

    signed_url_expiry_time = s3_setting.signed_url_expiry_time or 120

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_setting.aws_key,
        aws_secret_access_key=s3_setting.aws_secret,
        region_name=s3_setting.region_name,
    )

    params = {
        "Bucket": s3_setting.bucket_name,
        "Key": key,
    }

    if file_name:
        params["ResponseContentDisposition"] = f"filename={file_name}"

    return s3_client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=signed_url_expiry_time,
    )
