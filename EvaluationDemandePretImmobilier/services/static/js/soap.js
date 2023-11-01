function soumission() {

	console.log("Le client vient de soumettre une demande de prêt")
	
	var xmlhttp = new XMLHttpRequest();
    xmlhttp.open('POST', 'http://localhost:8000', true);
    // Exemple de requête SOAP
	const xmls = `
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.example.com/webservice">
   <soapenv:Header/>
   <soapenv:Body>
      <web:evaluationPret>
         <arg1>Value1</arg1>
         <arg2>Value2</arg2>
      </web:evaluationPret>
   </soapenv:Body>
</soapenv:Envelope>
`;

// Spécifiez l'URL du service SOAP
const url = 'http://localhost:8000/serviceComposite-wsdl';

// Envoyez la requête SOAP
const response = soapRequest({
  url: url,
  xml: xmls,
  headers: {
    'Content-Type': 'text/xml;charset=UTF-8',
  },
});

// Traitez la réponse SOAP
response.then((result) => {
  const { response } = result;
  console.log(response.body);
}).catch((error) => {
  console.error(error);
});

}
