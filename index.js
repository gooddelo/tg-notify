const express = require('express')
const cors = require('cors')
const axios = require('axios')

const app = express()
const port = 3000
const BOTTOKEN = process.env.BOTTOKEN
const GCAPTCHA = process.env.GCAPTCHA
const CHAT = process.env.CHAT

app.use(cors())

async function VerifyCAPTCHA(token) {
	let res = await axios.get(`https://www.google.com/recaptcha/api/siteverify?secret=${GCAPTCHA}&response=${token}`)
	return res.data.text
}

app.get('/', (req, res) => {
	res.send('<h1>Gooddelo API</h1><p>by Tojefin</p>')
})

app.post('/api/v1/sendform/', async (req, res) => {
	let { name, phone, email, comment, token, getstatus } = req.body

	if (!VerifyCAPTCHA(token)) {
		return res.status(401).end()
	}

	let text = `
	Получена заявка \n
	${req.get('Referrer')} \n
	👨: ${name} \n
	📞: ${phone} \n
	📧: ${email} \n
	📄: ${comment} 
	`

	await axios.get(`https://api.telegram.org/bot${BOTTOKEN}/sendMessage?text=${text}&chat_id=${CHAT}`)

	if (getstatus) {
		return res.json({ done: true })
	}

	return res.redirect('back')
})

app.listen(port, () => {
	console.log(`API listening on PORT ${port} `)
})

// Export the Express API
module.exports = app