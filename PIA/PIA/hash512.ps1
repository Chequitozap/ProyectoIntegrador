$mensaje =@("Funcion para ver el hash sha512")

function Ver-Hash{
 
    param([Parameter(Mandatory, ValueFromPipeline)] [string] $archivo)  

    $cinco = Get-FileHash -Algorithm SHA512 $archivo 

    $cinco > hash512.txt

}

$archivo = "$HOME\Documents\PIA\Modules\pageExtractor.py"

Ver-Hash -archivo $archivo

