export const readToken = (req, res, next) => {
    console.log("user token info: ", req.user);
    res.status(200).json(req.user);
}