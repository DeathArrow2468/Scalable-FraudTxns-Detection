$eventNumber = 1
Import-Csv .\paysim_shuffled.csv -Header step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest,isFraud,isFlaggedFraud |
Select-Object -Skip 1 -First 50000 | ForEach-Object{
$txn = @{

    event_number = $eventNumber
    step = [int]$_.step
    txn_id = [guid]::NewGuid().ToString()
   # user_id = $_.nameOrig #KAGGLE COLUMN: sender ID (for user velocity)
    type = [string]$_.type
    amount = [double]$_.amount
    nameOrig = $_.nameOrig
    nameDest = $_.nameDest
    oldbalanceOrg = [double]$_.oldbalanceOrg
    newbalanceOrig = [double]$_.newbalanceOrig
    oldbalanceDest = [double]$_.oldbalanceDest
    newbalanceDest = [double]$_.newbalanceDest
    timestamp = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
    #isFraud = [int]$_.isFraud
}

$jsonTxn = $txn | ConvertTo-Json -Compress

if ([string]::IsNullOrWhiteSpace($jsonTxn)){
    Write-Error "Invalid JSON generated: $jsonTxn"
    return
}

aws kinesis put-record --stream-name fraud-txns --partition-key $txn.nameOrig --data $jsonTxn --cli-binary-format raw-in-base64-out

Write-Host "Sending Event #$eventNumber : $($txn.nameOrig) -> $($txn.nameDest)"

$eventNumber++

Start-Sleep -Milliseconds 100 # 10 txns/sec
}