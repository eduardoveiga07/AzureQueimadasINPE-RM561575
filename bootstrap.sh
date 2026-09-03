#!/bin/bash
az login

RG_TFSTATE="rg-tfstate"
LOCATION="brazilsouth"
STORAGE_ACCOUNT="sttfstatequeimadas561575"
CONTAINER_NAME="tfstate"

az group create --name $RG_TFSTATE --location $LOCATION

az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RG_TFSTATE \
  --location $LOCATION \
  --sku Standard_LRS \
  --encryption-services blob

az storage container create \
  --name $CONTAINER_NAME \
  --account-name $STORAGE_ACCOUNT

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az ad sp create-for-rbac \
  --name "sp-monitor-queimadas" \
  --role Contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth > azure-credentials.json
