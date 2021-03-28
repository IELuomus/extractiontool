const res = await fetch(url, {
	method: 'POST', // Itse käyttäisin tässä juuri post, enkä get
	headers: {
		'Content-Type': 'application/json',
	}
	body: 'DATAA'
})