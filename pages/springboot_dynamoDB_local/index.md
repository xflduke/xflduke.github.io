# config dynamodb on centos memo

- [config dynamodb on centos](#config-dynamodb-on-centos)
  * [command memo](#command-memo)
  * [install dynamodb](#install-dynamodb)
  * [install aws cli2 and config keys](#install-aws-cli2-and-config-keys)

<a href="https://xflduke.github.io/">Back to Index</a>

## config dynamodb on centos 

### command memo

#### install dynamodb

```bash
wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
gunzip dynamodb_local_latest.tar.gz
mkdir ./dynamolocal
# (#__#)
tar -xvf dynamodb_local_latest.tar
mv DynamoDBLoca* ./dynamolocal/
mv LICENSE.txt ./dynamolocal/
mv README.txt ./dynamolocal/
java -Djava.library.path=./DynamoDBLocal_lib/ -jar DynamoDBLocal.jar -inMemory -sharedDb &
```

#### install aws cli2 and config keys

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws dynamodb list-tables --endpoint-url http://127.0.0.1:8000
aws configure
## sample input
# AWS Access Key ID [None]: fakeAWSAccessKey
# AWS Secret Access Key [None]: fakeAWSSecretAccessKey
# Default region name [None]: JP
# Default output format [None]: json
```

 <a href="#top">Back to top</a>

<a href="https://xflduke.github.io/">Back to Index</a>
